from django.core.management.base import BaseCommand

from baykeshop.conf import bayke_settings



class Command(BaseCommand):
    
    help = '创建测试数据'
    
    def add_arguments(self, parser) -> None:
        pass
    
    def handle(self, *args, **options):
        pass