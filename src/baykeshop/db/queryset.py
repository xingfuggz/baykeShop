from django.db import models


class BaseQuerySet(models.QuerySet):
    
    def delete(self):
        """ 逻辑删除 """
        return super().update(is_delete=True)
    
    def hard_delete(self):
        """ 物理删除 """
        return super().delete()
    
    def restore(self):
        """ 恢复删除 """
        return super().update(is_delete=False)
    
    def deleted(self):
        """ 已删除 """
        return self.filter(is_delete=True)
    
    def undeleted(self):
        """ 未删除 """
        return self.filter(is_delete=False)

    def all(self):
        return self.undeleted()