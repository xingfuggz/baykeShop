from django.core import management
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.models import Site

from baykeshop.contrib.system.models import BaykeDictModel


class Command(BaseCommand):
    help = _('Create a dictionary')

    def add_arguments(self, parser):
        parser.add_argument('site', type=int)   # site_id
        parser.add_argument('key', type=str)    # 键
        parser.add_argument('name', type=str)   # 名称
        parser.add_argument('value', type=str)  # 值

    def handle(self, *args, **options):
        site = self.create_site(options['site'])
        key = options['key']
        name = options['name']
        value = options['value']
        obj, iscreated = BaykeDictModel.objects.update_or_create(
            site=site, 
            key=key, 
            defaults={
                'name': name, 
                'value': value,
                'site': site, 
                'key': key, 
            }
        )
        _type = _('添加') if iscreated else _('更新')
        self.stdout.write(self.style.SUCCESS(_(f'{obj.name} { _type } 成功')))
        
    def create_site(self, site_id):
        """创建站点"""
        site = Site.objects.filter(id=site_id).first()
        if site:
            return site
        return Site.objects.create(name='bayke', domain='bayke.site')