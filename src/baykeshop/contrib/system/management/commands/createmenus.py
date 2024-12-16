from django.core import management
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission

from baykeshop.contrib.system.models import BaykeMenus


class Command(BaseCommand):
    help = "Create a menus"

    def handle(self, *args, **options):
        self.create_menus()

    def create_menus(self):
        menus = [
            {
                "name": "系统",
                "order": 4,
                "children": [
                    {
                        "name": "菜单管理",
                        "permission": "system.view_baykemenus"
                    },
                    {
                        "name": "字典管理",
                        "permission": "system.view_baykedict"
                    },
                    {
                        "name": "站点设置",
                        "permission": "sites.view_site"
                    },
                    {
                        "name": "轮播图管理",
                        "permission": "system.view_baykebanners"
                    }
                ]
            },
            {
                "name": "商品",
                "order": 1,
                "children": [
                    {
                        "name": "商品分类",
                        "permission": "shop.view_baykeshopcategory"
                    },
                    {
                        "name": "商品管理",
                        "permission": "shop.view_baykeshopgoods"
                    },
                    {
                        "name": "商品规格",
                        "permission": "shop.view_baykeshopspec"
                    },
                    {
                        "name": "品牌管理",
                        "permission": "shop.view_baykeshopbrand"
                    },
                ]
            },
            {
                "name": "订单",
                "order": 2,
                "children": [
                    {
                        "name": "订单管理",
                        "permission": "shop.view_baykeshoporders"
                    },
                    {
                        "name": "订单评论",
                        "permission": "shop.view_baykeshoporderscomment"
                    },
                ]
            },
            {
                "name": "用户",
                "order": 3,
                "children": [
                    {
                        "name": "用户管理",
                        "permission": "auth.view_user"
                    },
                    {
                        "name": "用户组",
                        "permission": "auth.view_group"
                    },
                ]
            },
            {
                "name": "内容",
                "order": 5,
                "children": [
                    {
                        "name": "文章分类",
                        "permission": "article.view_baykearticlecategory"
                    },
                    {
                        "name": "文章管理",
                        "permission": "article.view_baykearticlecontent"
                    },
                    {
                        "name": "标签管理",
                        "permission": "article.view_baykearticletags"
                    },
                    {
                        "name": "侧边栏",
                        "permission": "article.view_baykesidebar"
                    },
                ]
            },
        ]

        for menu in menus:
            menu_obj, iscreated = BaykeMenus.objects.update_or_create(
                name=menu["name"],
                defaults={
                    "name": menu["name"],
                    "order": menu["order"]
                }
            )
            status = '添加' if iscreated else '更新'
            self.stdout.write(self.style.SUCCESS(f'{menu_obj.name} { status } 成功'))

            for child in menu["children"]:
                app_label, codename = child["permission"].split(".")
                permission_obj = Permission.objects.filter(
                    codename=codename, 
                    content_type__app_label=app_label
                )
                if not permission_obj.exists(): continue
                child_obj, _iscreated = BaykeMenus.objects.update_or_create(
                    parent=menu_obj, 
                    name=child["name"], 
                    defaults={
                        "name": child["name"],
                        "parent": menu_obj,
                        "permission": permission_obj.first()
                    }
                )
                status = '添加' if _iscreated else '更新'
                self.stdout.write(self.style.SUCCESS(f'{child_obj.name} { status } 成功'))