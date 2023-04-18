from django.contrib import admin

from baykeshop.module.user.models import BaykeUserInfo
from baykeshop.module.admin.models import BaykePermission
from baykeshop.module.admin.options import StackedInline, TabularInline

class BaykeUserInfoInline(StackedInline):
    '''Tabular Inline View for BaykeUserInfo'''
    model = BaykeUserInfo
    

class BaykePermissionInline(TabularInline):
    '''Tabular Inline View for BaykePermission'''

    model = BaykePermission
    min_num = 1
    max_num = 20
    extra = 1
    # raw_id_fields = (,)