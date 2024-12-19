from django.db import models
from .queryset import BaseQuerySet


class BaseManager(models.Manager):
    def get_queryset(self):
        """ 重写父类方法 """
        return BaseQuerySet(self.model, using=self._db)
    
    def delete(self):
        """ 逻辑删除 """
        return self.get_queryset().delete()
    
    def hard_delete(self):
        """ 物理删除 """
        return self.get_queryset().hard_delete()
    
    def restore(self):
        """ 恢复删除 """
        return self.get_queryset().restore()
    
    def deleted(self):
        """ 已删除 """
        return self.get_queryset().deleted()
    
    def all(self):
        """ 未删除 """
        return self.get_queryset().all()
    
    