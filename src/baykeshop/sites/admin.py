from django.contrib import admin
from django.urls import reverse, NoReverseMatch

from baykeshop.forms import ModelForm
from baykeshop.contrib.system.models import BaykeDictModel
from baykeshop.db.analysis import (
    UserAnalysisService,
    OrderAnalysisService,
    VisitAnalysisService,
)
from baykeshop.conf import bayke_settings
from baykeshop.contrib.system.models import BaykeMenus
from baykeshop.contrib.shop.models import BaykeShopOrders
from .echarts import orders_chart, users_chart, user_pie_chart


class TabularInline(admin.TabularInline):
    """Tabular Inline View for"""
    form = ModelForm


class StackedInline(admin.StackedInline):
    """Stacked Inline View for"""
    form = ModelForm


class ModelAdmin(admin.ModelAdmin):
    """自定义ModelAdmin"""
    form = ModelForm


class AdminSite(admin.AdminSite):
    """自定义AdminSite"""

    index_template = "baykeshop/admin/index.html"

    @property
    def site_header(self):
        return BaykeDictModel.get_key_value("SITE_HEADER")

    @property
    def site_title(self):
        return BaykeDictModel.get_key_value("SITE_TITLE")

    @property
    def index_title(self):
        return BaykeDictModel.get_key_value("INDEX_TITLE")

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        # 用户分析
        user_analysis = UserAnalysisService(request)
        user_data = user_analysis.get_data("%m-%d")
        # 订单分析
        order_analysis = OrderAnalysisService(model=BaykeShopOrders)
        # 订单销售分析
        order_data = order_analysis.get_data("%m-%d")
        sales_data = order_analysis.get_sales_data("%m-%d")
        # 访问分析
        visit_analysis = VisitAnalysisService()
        visit_data = visit_analysis.get_data("%m-%d")

        extra_context = {
            "order_data": order_data,
            "sales_data": sales_data,
            "user_data": user_data,
            "visit_data": visit_data,
            "orders_chart": orders_chart(),
            "users_chart": users_chart(),
            "user_pie_chart": user_pie_chart(),
        }
        return super().index(request, extra_context)

    def each_context(self, request):
        context = super().each_context(request)
        if bayke_settings.USE_MENU:
            context["available_apps"] = self.get_menus(request)
        return context

    def get_menus(self, request):
        # 获取用户的所有权限菜单，页面默认显示view菜单名称
        perms = request.user.get_all_permissions()
        menus_dict = {}
        for perm in perms:
            app_label, codename = tuple(perm.split('.')) 
            menu_qs = BaykeMenus.objects.filter(
                permission__content_type__app_label=app_label, 
                permission__codename=codename,
                parent__isnull=False,
                is_show=True
            )
            if menu_qs.exists():
                _menu = menu_qs.first()
                # model模型
                model = _menu.permission.content_type.model_class()
                is_registered = self.is_registered(_menu.permission.content_type.model_class())
                # 未在admin中注册则跳出循环
                if not is_registered: continue
                # 获取注册的ModelAdmin
                model_admin = self._registry[model]
                # 获取权限
                perms = model_admin.get_model_perms(request)
                # url参数
                info = (app_label, model._meta.model_name)
                if _menu.parent not in menus_dict:
                    menus_dict[_menu.parent] = []
                    menus_dict[_menu.parent].append(_menu)
                else:
                    menus_dict[_menu.parent].append(_menu)

        menus = []

        for parent, values in menus_dict.items():
            model_dict = {
                "name": parent.name,
                "icon": parent.icon,
                "order": parent.order,
                "models": self.get_models(request, values),
            }
            menus.append(model_dict)
        menus = sorted(menus, key=lambda x: x["order"])
        return menus

    def get_models(self, request, values):
        menus = []
        for menu in values:
            item = {}
            item["name"] = menu.name
            item["icon"] = menu.icon
            item["order"] = menu.order
            item["model"] = menu.permission.content_type.model_class()
            item["perms"] = self._registry[item["model"]].get_model_perms(request)
            item["object_name"] = item["model"]._meta.object_name
            app_label = menu.permission.content_type.app_label
            info = (app_label, item["model"]._meta.model_name)
            if item["perms"].get("change") or item["perms"].get("view"):
                item["view_only"] = not item["perms"].get("change")
                try:
                    item["admin_url"] = reverse(
                        "admin:%s_%s_changelist" % info, current_app=self.name
                    )
                except NoReverseMatch:
                    pass
            
            if item["perms"].get("add"):
                try:
                    item["add_url"] = reverse(
                        "admin:%s_%s_add" % info, current_app=self.name
                    )
                except NoReverseMatch:
                    pass
            menus.append(item)
        menus = sorted(menus, key=lambda x: x["order"])
        return menus


admin_site = AdminSite(name="baykeshop")
