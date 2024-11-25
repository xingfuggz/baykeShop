from django.contrib import admin
from baykeshop.config.settings import bayke_settings as config
from baykeshop.apps.core.utils.analyse import (
    VisitsAnalysis, UsersAnalysis, OrdersAnalysis
)

class AdminSite(admin.AdminSite):
    """ 自定义后台管理站点 """
    site_header = config.SITE_HEADER
    site_title = config.SITE_TITLE
    index_title = config.INDEX_TITLE

    index_template = 'core/admin/index.html'

    def each_context(self, request):
        context = super().each_context(request)
        # 订单相关分析
        orders_analysis = OrdersAnalysis(request)
        context['orders_today_amount'] = orders_analysis.orders_today_amount()
        context['orders_yesterday_amount'] = orders_analysis.orders_yesterday_amount()
        context['orders_amount_ratio'] = orders_analysis.orders_amount_ratio()
        context['orders_month_amount'] = orders_analysis.orders_month_amount()
        # 订单量
        context['orders_today_count'] = orders_analysis.orders_today_count()
        context['orders_yesterday_count'] = orders_analysis.orders_yesterday_count()
        context['orders_count_ratio'] = orders_analysis.orders_count_ratio()
        context['orders_month_count'] = orders_analysis.orders_month_count()
        context['orders_chart_30days'] = orders_analysis.get_30days_orders_chart()
        
        # 访问相关分析
        visits_analysis = VisitsAnalysis(request)
        context['visits_today_pv_count'] = visits_analysis.visits_today_pv_count()
        context['visits_yesterday_pv_count'] = visits_analysis.visits_yesterday_pv_count()
        context['visits_month_pv_count'] = visits_analysis.visits_month_pv_count()
        context['visits_pv_ratio'] = visits_analysis.visits_pv_ratio()
        # 用户相关分析
        users_analysis = UsersAnalysis(request)
        context['users_today_count'] = users_analysis.users_today_count()
        context['users_yesterday_count'] = users_analysis.users_yesterday_count()
        context['users_month_count'] = users_analysis.users_month_count()
        context['users_today_ratio'] = users_analysis.users_today_ratio()
        context['users_chart'] = users_analysis.get_users_chart()
        context['user_percentage_chart'] = users_analysis.user_percentage_chart()
        return context


site = AdminSite(name='bayke_admin')
