from baykeshop.contrib.shop.apps import ShopConfig
from baykeshop.contrib.member.apps import MemberConfig
from baykeshop.contrib.gallery.apps import GalleryConfig
from baykeshop.contrib.system.apps import SystemConfig

INSTALLED_APPS = [
    ShopConfig.name,
    MemberConfig.name,
    GalleryConfig.name,
    SystemConfig.name,
]