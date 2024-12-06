from django.contrib import admin
from baykeshop.forms import ModelForm
from baykeshop.contrib.system.models import BaykeDictModel
from baykeshop.db.analysis import  UserAnalysisService, OrderAnalysisService, VisitAnalysisService
from baykeshop.contrib.shop.models import BaykeShopOrders
from .echarts import orders_chart, users_chart, user_pie_chart


class TabularInline(admin.TabularInline):
    '''Tabular Inline View for '''
    form = ModelForm


class StackedInline(admin.StackedInline):
    '''Stacked Inline View for '''
    form = ModelForm


class ModelAdmin(admin.ModelAdmin):
    """自定义ModelAdmin"""
    form = ModelForm


class AdminSite(admin.AdminSite):
    """ 自定义AdminSite """

    index_template = 'baykeshop/admin/index.html'

    @property
    def site_header(self):
        return BaykeDictModel.get_key_value('SITE_HEADER')
    
    @property
    def site_title(self):
        return BaykeDictModel.get_key_value('SITE_TITLE')
    
    @property
    def index_title(self):
        return BaykeDictModel.get_key_value('INDEX_TITLE')

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        # 用户分析
        user_analysis = UserAnalysisService(request)
        user_data = user_analysis.get_data('%m-%d')
        # 订单分析
        order_analysis = OrderAnalysisService(model=BaykeShopOrders)
        # 订单销售分析
        order_data = order_analysis.get_data('%m-%d')
        sales_data = order_analysis.get_sales_data('%m-%d')
        # 访问分析
        visit_analysis = VisitAnalysisService()
        visit_data = visit_analysis.get_data('%m-%d')
        # orders_chart()
        
        extra_context = {
            "order_data": order_data,
            "sales_data": sales_data,
            "user_data": user_data,
            "visit_data": visit_data,
            "orders_chart": orders_chart(),
            "users_chart": users_chart(),
            "user_pie_chart": user_pie_chart(),
        }
        return super().index(request, extra_context)
    

admin_site = AdminSite(name="baykeshop")

