from baykeshop.contrib.shop.apps import ShopConfig
from baykeshop.contrib.member.apps import MemberConfig
from baykeshop.contrib.system.apps import SystemConfig
from baykeshop.contrib.article.apps import ArticleConfig

INSTALLED_APPS = [
    ShopConfig.name,
    MemberConfig.name,
    SystemConfig.name,
    ArticleConfig.name,
]