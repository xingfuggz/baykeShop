from django.db import models
from django.utils.translation import gettext_lazy as _

from baykeshop.apps.core.validators import validate_image_size
from .abstract import BaseModel


class UploadImage(BaseModel):
    """
    上传图片
    """
    file = models.ImageField(
        upload_to='upload/%Y/%m/%d', 
        verbose_name=_('文件'), 
        validators=[validate_image_size]
    )

    class Meta:
        verbose_name = _('上传图片')
        verbose_name_plural = verbose_name
        ordering = ['-create_time']
    
    def __str__(self):
        return self.file.name
    
    def get_file_url(self):
        return self.file.url
    
    def get_file_name(self):
        return self.file.name.split('/')[-1]
    
    def get_file_size(self):
        return self.file.size
