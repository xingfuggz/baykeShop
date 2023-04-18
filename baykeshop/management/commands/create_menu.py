from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission

from baykeshop.conf import bayke_settings
from baykeshop.module.admin.models import BaykeMenu, BaykePermission


MENUS = (
    bayke_settings.ADMIN_MENUS_DATAS or 
    [
        {
            'name': '订单',
            'sort': 3,
            'perms': ['view_baykeorderinfo']
        },
        {
            'name': '商品',
            'sort': 4,
            'perms':['view_baykecategory', 'view_baykespec', 'view_baykegoods', 'view_baykebanner', 'view_baykeorderinfocomments']
        },
        {
            'name': '认证和授权',
            'sort': 1,
            'perms': ['view_group', 'view_user', 'view_baykemenu', 'view_logentry']
        },
        {
            'name': '内容',
            'sort': 2,
            'perms': ['view_baykearticlecategory', 'view_baykearticle']
        }
    ]
)


class Command(BaseCommand):
    
    help = '创建后台自定义菜单'
    menus = MENUS
    
    def add_arguments(self, parser) -> None:
        pass
        # parser.add_argument(
        #     "--delete",
        #     action="store_true",
        #     help="Delete poll instead of closing it",
        # )
        
    def handle(self, *args, **options):
        if not isinstance(MENUS, (list, tuple)):
            self.stdout.write(self.style.ERROR(f'MENUS的值为{MENUS}，不可迭代，应该为list或tuple类型'))
        for menu in self.menus:
            try:
                m, c = BaykeMenu.objects.update_or_create(name=menu['name'], defaults={'name': menu['name'], 'sort': menu['sort']})
                for perm in menu['perms']:
                    perm_obj = Permission.objects.get(codename=perm)
                    BaykePermission.objects.update_or_create(permission=perm_obj, menus=m, defaults={'permission': perm_obj})
                    message = "创建" if c else "更新"
                    self.stdout.write(self.style.SUCCESS(f'{menu["name"]}-菜单{message}成功！'))
            except KeyError:
                self.stdout.write(self.style.ERROR(f'相关键不存在,请检查格式'))
        
        