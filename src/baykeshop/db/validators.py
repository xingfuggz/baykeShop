from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from baykeshop.conf import bayke_settings

def validate_phone(value):
    # 中国区手机号验证
    validators.RegexValidator(
        bayke_settings.REGEX_PHONE, 
        _("手机号码格式有误"), 
        "invalid"
    )(value)


def validate_image_size(value):
    """ 对图片大小进行验证 """
    if value.size > bayke_settings.MAX_IMAGE_SIZE:
        raise ValidationError(
            _("图片大小超过限制"), 
            code='invalid'
        )