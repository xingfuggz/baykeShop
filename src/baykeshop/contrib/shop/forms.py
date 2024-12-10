import json
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import widgets
from baykeshop.forms import ModelForm
from .models import BaykeShopGoodsSKU, BaykeShopSpec


class MyFilteredSelectMultiple(widgets.FilteredSelectMultiple):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        if value is not None:
            if isinstance(value, str):
                try:
                    value = json.loads(value)
                    value = [int(v["id"]) for v in value]
                except (json.JSONDecodeError, ValueError):
                    value = []
            elif isinstance(value, list):
                value = [int(v) for v in value]
            else:
                value = [v.pk for v in value]
        context["widget"]["value"] = value
        return context


class BaykeShopGoodsSKUForm(ModelForm):
    """商品SKU表单"""

    specs = forms.ModelMultipleChoiceField(
        queryset=BaykeShopSpec.get_queryset().filter(parent__isnull=False),
        label=_("商品规格"),
        widget=MyFilteredSelectMultiple(_("商品规格"), False),
        required=False,
        help_text=_("单规格时可以不选； 多规格时必选且同一个规格下只能选一个规格值"),
    )

    class Meta:
        model = BaykeShopGoodsSKU
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 初始化规格值回显
        if self.instance and self.instance.specs:
            try:
                specs_ids = [spec["id"] for spec in json.loads(self.instance.specs)]
                self.initial["specs"] = BaykeShopSpec.get_queryset().filter(
                    id__in=specs_ids
                )
            except (json.JSONDecodeError, ValueError):
                self.initial["specs"] = []

    def clean_specs(self):
        specs = self.cleaned_data.get("specs")
        if specs.exists():
            values = specs.values("id", "parent__name", "name")
            # 父级名称
            parent_names = [spec["parent__name"] for spec in values]
            if specs.count() > len(set(parent_names)):
                raise forms.ValidationError(_("同一个规格下只能选一个规格值"))

            json_data = json.dumps(list(values), ensure_ascii=False)
            specs = json_data
            return specs
        return json.dumps([], ensure_ascii=False)
