from django.contrib import admin

from baykeshop.module.user.models import BaykeUserInfo
from baykeshop.module.admin.models import BaykePermission

class BaykeUserInfoInline(admin.StackedInline):
    '''Tabular Inline View for BaykeUserInfo'''
    model = BaykeUserInfo
    

class BaykePermissionInline(admin.TabularInline):
    '''Tabular Inline View for BaykePermission'''

    model = BaykePermission
    min_num = 1
    max_num = 20
    extra = 1
    # raw_id_fields = (,)