from django.core.management.base import BaseCommand
from django.core import management
from django.conf import settings


class Command(BaseCommand):
    
    help = '创建测试数据'
    
    def add_arguments(self, parser) -> None:
        pass
    
    def handle(self, *args, **options):
        baykebanner = f"{settings.BASE_DIR}/baykeshop/conf/test/baykebanner.json"
        baykecategory = f"{settings.BASE_DIR}/baykeshop/conf/test/baykecategory.json"
        baykespec = f"{settings.BASE_DIR}/baykeshop/conf/test/baykespec.json"
        baykespecoptions = f"{settings.BASE_DIR}/baykeshop/conf/test/baykespecoptions.json"
        baykegoods = f"{settings.BASE_DIR}/baykeshop/conf/test/baykegoods.json"
        baykegoodsbanners = f"{settings.BASE_DIR}/baykeshop/conf/test/baykegoodsbanners.json"
        baykeproduct = f"{settings.BASE_DIR}/baykeshop/conf/test/baykeproduct.json"
        management.call_command('loaddata', baykebanner, verbosity=0)
        management.call_command('loaddata', baykecategory, verbosity=0)
        management.call_command('loaddata', baykespec, verbosity=0)
        management.call_command('loaddata', baykespecoptions, verbosity=0)
        management.call_command('loaddata', baykegoods, verbosity=0)
        management.call_command('loaddata', baykegoodsbanners, verbosity=0)
        management.call_command('loaddata', baykeproduct, verbosity=0)
        self.stdout.write(self.style.SUCCESS("演示数据创建成功！"))