from django.db import models
from django.db.models.functions import Coalesce
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.cache import cache
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from baykeshop.db import BaseModel


class VisitManager(models.Manager):
    def create_pv_uv(self, request, content_object: models.Model):
        """创建PV和UV数据"""
        ip = self.get_client_ip(request)
        date = timezone.now().date()
        content_type = ContentType.objects.get_for_model(content_object)
        try:
            obj = self.get(
                ip=ip, date=date, 
                content_type=content_type, 
                object_id=content_object.id
            )
            if cache.get(f'{ip}-{date}-{content_object.pk}') is None:
                # 第二次创建缓存1小时
                cache.set(f'{ip}-{date}-{content_object.pk}', True, 60 * 60)
                obj.pv = models.F('pv') + 1
                obj.save()
                
        except self.model.DoesNotExist:
            obj = self.create(
                ip=ip, date=date, 
                content_type=content_type, 
                object_id=content_object.id,
                pv=1,
                uv=1
            )
            # 第一次创建缓存10分钟
            cache.set(f'{ip}-{date}-{content_object.pk}', True, 60 * 10)
        return obj
    
    def get_uv_pv_count(self, content_object: models.Model):
        """获取UV数量"""
        content_type = ContentType.objects.get_for_model(content_object)
        object_id = content_object.id
        queryset = self.filter(content_type=content_type, object_id=object_id)
        count_aggregate = queryset.aggregate(
            uv=Coalesce(models.Sum('uv'), 0),
            pv=Coalesce(models.Sum('pv'), 0)
        )
        return count_aggregate
    
    @staticmethod
    def get_client_ip(request):
        """获取客户端IP地址"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    

class Visit(BaseModel):
    """分析数据模型"""
    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE, 
        verbose_name=_('内容类型')
    )
    object_id = models.PositiveBigIntegerField(verbose_name=_('对象ID'))
    content_object = GenericForeignKey('content_type', 'object_id')
    ip = models.GenericIPAddressField(verbose_name=_('IP'), default='127.0.0.1')
    pv = models.PositiveBigIntegerField(verbose_name=_('PV'))
    uv = models.PositiveBigIntegerField(verbose_name=_('UV'))
    date = models.DateField(verbose_name=_('日期'))

    objects = VisitManager()

    class Meta:
        verbose_name = _('分析数据')
        verbose_name_plural = verbose_name
        ordering = ['-date']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['content_type', 'object_id', 'date']),
        ]        

    def __str__(self):
        return f"{self.content_object} / {self.date} / {self.pv} / {self.uv}"