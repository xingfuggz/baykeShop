import re
import json

from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def is_bool(value):
    """
    验证值是否为布尔值
    :param value: 值
    :return: 布尔值
    """
    if value.lower() in ["true", "false"]:
        return True
    return False


def is_dict(value):
    """
    验证值是否为字典
    :param value: 值
    :return: 布尔值
    """
    if all(re.match(r"^\s*\w+\s*:\s*.+\s*$", line) for line in value.splitlines()):
        return True
    return False


def is_list(value):
    """
    验证值是否为列表
    :param value: 值
    :return: 布尔值
    """

    if all(re.match(r"^\s*.+\s*$", line) for line in value.splitlines()):
        return True
    return False


def is_json(value):
    """
    验证值是否为JSON对象
    :param value: 值
    :return: 布尔值
    """
    try:
        json.loads(value)
        return True
    except json.JSONDecodeError:
        return False


def validate_dict_value(value):
    # 布尔值验证
    if is_bool(value):
        return True

    # 键值对验证
    if is_dict(value):
        return True

    # 列表验证
    if is_list(value):
        return True

    # JSON 对象验证
    if is_json(value):
        return True

    raise ValidationError(
        _("%(value)s is not valid"),
        params={"value": value},
        code="invalid",
    )
