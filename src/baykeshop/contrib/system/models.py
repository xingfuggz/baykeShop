import re
import json

from django.db import models
from django.utils.translation import gettext_lazy as _
from .validators import (
    validate_dict_value, is_bool, is_dict, is_json, is_list
)

from baykeshop.db import BaseModel


class BaykeDictModel(BaseModel):
    """ 字典管理  """
    name = models.CharField(max_length=50, verbose_name=_('名称'))
    key = models.SlugField(max_length=50, verbose_name=_('键'))
    value = models.TextField(
        verbose_name=_('值'), 
        help_text=_('''
            布尔值：True/False; 
            键值对：key1:value1一行一对;
            list:value1,value2一行一个值;
            json:{"key1":"value1"}
        ''' ), 
        validators=[validate_dict_value]
    )

    class Meta:
        verbose_name = _('字典管理')
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
        constraints = [
            models.UniqueConstraint(fields=['key', 'site'], name='unique_key_site')
        ]

    def __str__(self):
        return self.name
    
    @classmethod
    def get_key_value(cls, key, site_id=1):
        """ 获取字典值 """
        try:
            obj = cls.objects.get(key=key, site__id=site_id)
            if is_bool(obj.value):
                _v = json.loads(obj.value.lower())
                return _v
            if is_dict(obj.value):
                values = obj.value.splitlines()
                _v = {}
                for item in values:
                    k, v = item.split(':')
                    _v[k] = v
                return _v
            if is_list(obj.value) and obj.value.splitlines().__len__() == 1:
                return obj.value
            if is_list(obj.value) and obj.value.splitlines().__len__() > 1:
                return obj.value.splitlines()
            if is_json(obj.value):
                return json.loads(obj.value)
        except cls.DoesNotExist:
            return None
    
    def save(self, *args, **kwargs):
        self.get_key_value('a')
        super().save(*args, **kwargs)
