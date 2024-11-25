from django.db import models
from django.db.models.functions import TruncDate
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from pyecharts.charts import Bar, Line
from pyecharts import options as opts
from pyecharts.globals import ThemeType

from baykeshop.apps.order.models import BaykeShopOrder
from baykeshop.apps.core.models import Visit


User = get_user_model()


class AnalysisService:
    """分析服务"""
    
    def __init__(self, request=None):
        self.request = request

    @property
    def _today(self):
        return timezone.now().date()
    
    @property
    def _yesterday(self):
        return self._today - timezone.timedelta(days=1)
    
    # 获取当月天数列表
    def get_month_dates(self):
        """ 获取当月1日到最后一日的日期列表 """
        import calendar
        _, last_day = calendar.monthrange(self._today.year, self._today.month)
        first_day = self._today.replace(day=1)
        last_day_date = self._today.replace(day=last_day)
        date_list = []
        current_date = first_day
        while current_date <= last_day_date:
            date_list.append(current_date)
            current_date += timezone.timedelta(days=1)
        return date_list

    # 最近七日日期列表
    def get_week_dates(self, days=7):
        week_dates = []
        for i in range(days):
            week_dates.append(self._today - timezone.timedelta(days=i))
        return week_dates


class UsersAnalysis(AnalysisService):
    """ 用户分析 """
    def users_queryset(self):
        """ 用户queryset """
        queryset = User.objects.alias(date=TruncDate('date_joined')).annotate(date=models.F('date'))
        return queryset

    def users_count(self):
        """ 用户总数 """
        return self.users_queryset().count()
    
    def users_today_count(self):
        """ 今日新增用户数 """
        return self.users_queryset().filter(date_joined__date=self._today).count()
    
    def users_yesterday_count(self):
        """ 昨日新增用户数 """
        return self.users_queryset().filter(date_joined__date=self._yesterday).count()
    
    def users_week_count(self):
        """ 本周新增用户数 """
        return self.users_queryset().filter(
            date__range=(self._today - timezone.timedelta(days=6), self._today)
            ).count()
    
    def users_month_count(self):
        """ 本月新增用户数 """
        qs = self.users_queryset().filter(
            date__range=(self._today.replace(day=1), self._today)
        )
        return qs.count()
    
    def users_year_count(self):
        """ 本年新增用户数 """
        return self.users_queryset().filter(
            date_joined__range=(self._yesterday.replace(month=1, day=1), self._yesterday)
        ).count()
    
    # 日环比
    def users_today_ratio(self):
        """ 今日用户数环比 """
        today_count = self.users_today_count() 
        yesterday_count = self.users_yesterday_count()
        if yesterday_count == 0: return 0
        growth_rate = (today_count - yesterday_count) / yesterday_count
        return round(growth_rate, 2) * 100
    
    def get_users_chart_data(self):
        """ 用户趋势图 """
        queryset = self.users_queryset()
        dates = self.get_week_dates()
        results = [
            {
                'date': date.strftime('%m-%d'), 
                'count': queryset.filter(date=date).count()
            } 
            for date in dates
        ]
        return results

    def get_users_chart(self):
        """ 用户访问趋势图 """
        datas = self.get_users_chart_data()
        x_data = [item['date'] for item in datas]
        y_data = [item['count'] for item in datas]
        c = (
            Line(init_opts=opts.InitOpts(
                    width="calc(100% - 100px);", 
                    # width="100%",
                    height="300px", 
                    theme=ThemeType.WALDEN,
                    js_host="/static/core/js/"
                    # bg_color="#F8F8F8",
                ))
            .add_xaxis(x_data)
            .add_yaxis("", y_data, is_smooth=True)
            .set_series_opts(
                areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
                label_opts=opts.LabelOpts(is_show=False),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title="用户统计", pos_left="30"),
                xaxis_opts=opts.AxisOpts(
                    axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                    is_scale=False,
                    boundary_gap=False,
                ),
            )
            .render_embed()
        )
        return c

    def user_percentage_ratio(self):
        """ 用户访问比例 """
        # 本月新增用户总数（100%）
        month_count = self.users_month_count()
        # 本月下单用户（留存客户）
        month_pay_order_queryset = self.users_queryset().filter(
            date__range=(self._today.replace(day=1), self._today)
        ).filter(baykeshoporder__isnull=False)
        # 本月下单用户总数
        month_pay_order_count = month_pay_order_queryset.count()
        # 本月下单用户ids
        month_pay_user_ids = month_pay_order_queryset.values_list('id', flat=True)
        # 回流用户(当月下单用户里边是否在过去下过订单的用户)
        past_user = self.users_queryset().filter(
            date__lt=self._today.replace(day=1)
        ).filter(baykeshoporder__isnull=False, id__in=month_pay_user_ids)
        # 回流用户数
        reflux_ount = past_user.count()
        # 未消费用户数
        no_order_count = month_count - month_pay_order_count
        # 消费一次的用户数
        one_order_count = 0
        for item in month_pay_order_queryset:
            if item.baykeshoporder_set.count() == 1:
                one_order_count += 1
        
        return [
            ['留存客户', month_pay_order_count], 
            ['消费一次客户', one_order_count], 
            ['回流客户', reflux_ount], 
            ['未消费客户', no_order_count]
        ]

    def user_percentage_chart(self):
        from pyecharts.charts import Pie
        datas = self.user_percentage_ratio()
        c = (
            Pie(init_opts=opts.InitOpts(
                    width="calc(100% - 100px);", 
                    # width="100%",
                    height="300px", 
                    theme=ThemeType.WALDEN,
                    js_host="/static/core/js/"
                    # bg_color="#F8F8F8",
                ))
            .add(
                "",
                datas,
                center=["58%", "58%"],
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title=_("当月购买用户统计")),
                legend_opts=opts.LegendOpts(pos_left="50%"),
            )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        ).render_embed()
        return c


class VisitsAnalysis(AnalysisService):
    """ 访问分析 """
    def visits_queryset(self):
        """ 访问queryset """
        queryset = Visit.objects.all()
        return queryset
    
    def visits_pv_count(self):
        """ 访问pv总数 """
        return self.visits_queryset().aggregate(models.Sum("pv"))["pv__sum"] or 0
    
    def visits_uv_count(self):
        """ 访问uv总数 """
        return self.visits_queryset().aggregate(models.Sum("uv"))["uv__sum"] or 0
    
    def visits_today_pv_count(self):
        """ 今日pv访问数 """
        return self.visits_queryset().filter(date=self._today).aggregate(models.Sum("pv"))["pv__sum"] or 0
    
    def visits_today_uv_count(self):
        """ 今日uv访问数 """
        return self.visits_queryset().filter(date=self._today).aggregate(models.Sum("uv"))["uv__sum"] or 0
    
    def visits_yesterday_pv_count(self):
        """ 昨日pv访问数 """
        return self.visits_queryset().filter(date=self._yesterday).aggregate(models.Sum("pv"))["pv__sum"] or 0
    
    def visits_yesterday_uv_count(self):
        """ 昨日uv访问数 """
        return self.visits_queryset().filter(date=self._yesterday).aggregate(models.Sum("uv"))["uv__sum"] or 0
    
    def visits_week_pv_count(self):
        """ 本周pv访问数 """
        return self.visits_queryset().filter(
            date__range=(self._yesterday - timezone.timedelta(days=6), self._yesterday)
        ).aggregate(models.Sum("pv"))["pv__sum"] or 0
    
    def visits_week_uv_count(self):
        """ 本周uv访问数 """
        return self.visits_queryset().filter(
            date__range=(self._yesterday - timezone.timedelta(days=6), self._yesterday)
        ).aggregate(models.Sum("uv"))["uv__sum"] or 0
    
    def visits_month_pv_count(self):
        """ 本月pv访问数 """
        return self.visits_queryset().filter(
            date__range=(self._today.replace(day=1), self._today)
        ).aggregate(models.Sum("pv"))["pv__sum"] or 0
    
    def visits_month_uv_count(self):
        """ 本月uv访问数 """
        return self.visits_queryset().filter(
            date__range=(self._yesterday.replace(day=1), self._yesterday)
        ).aggregate(models.Sum("uv"))["uv__sum"] or 0
    
    def visits_year_pv_count(self):
        """ 本年pv访问数 """
        return self.visits_queryset().filter(
            date__range=(self._yesterday.replace(month=1, day=1), self._yesterday)
        ).aggregate(models.Sum("pv"))["pv__sum"] or 0
    
    def visits_year_uv_count(self):
        """ 本年uv访问数 """
        return self.visits_queryset().filter(
            date__range=(self._yesterday.replace(month=1, day=1), self._yesterday)
        ).aggregate(models.Sum("uv"))["uv__sum"]
    
    def visits_pv_ratio(self):
        """ 今日pv访问数环比 """
        today_count = self.visits_today_pv_count() 
        yesterday_count = self.visits_yesterday_pv_count()
        if yesterday_count == 0: return 0
        growth_rate = (today_count - yesterday_count) / yesterday_count
        return round(growth_rate, 2)
    
    def visits_uv_ratio(self):
        """ 今日uv访问数环比 """
        today_count = self.visits_today_uv_count() 
        yesterday_count = self.visits_yesterday_uv_count()
        if yesterday_count == 0: return 0
        growth_rate = (today_count - yesterday_count) / yesterday_count
        return round(growth_rate, 2)
    

class OrdersAnalysis(AnalysisService):
    """ 订单分析 """
    def orders_queryset(self):
        """ 全部订单queryset """
        queryset = BaykeShopOrder.objects.all()
        return queryset
    
    def orders_paid_aueryset(self):
        """ 已支付订单 """
        return self.orders_queryset().filter(
            (models.Q(status__gt=0) & models.Q(status__lt=5)) | 
            models.Q(is_verify=True)
        )
    
    def orders_count(self):
        """ 订单总数,含未支付订单 """
        return self.orders_queryset().count()
    
    def orders_amount(self):
        """ 销售总金额，已支付订单 """
        pay_price__sum = self.orders_paid_aueryset().aggregate(models.Sum("pay_price"))["pay_price__sum"]
        return pay_price__sum or 0
    
    # 今日销售总额
    def orders_today_amount(self):
        pay_price__sum = self.orders_paid_aueryset().filter(
            create_time__date=self._today).aggregate(
                models.Sum("pay_price")
            )["pay_price__sum"]
        return pay_price__sum or 0
          
    # 昨日销售总额
    def orders_yesterday_amount(self):
        pay_price__sum =  self.orders_paid_aueryset().filter(
            create_time__date=self._yesterday
        ).aggregate(models.Sum("pay_price"))["pay_price__sum"]
        return pay_price__sum or 0
    
    # 本周销售总额
    def orders_week_amount(self):
        return self.orders_paid_aueryset().filter(
            create_time__range=(self._yesterday - timezone.timedelta(days=6), self._yesterday)
        ).aggregate(models.Sum("pay_price"))["pay_price__sum"] or 0
    
    # 本月销售总额
    def orders_month_amount(self):
        qs = self.orders_paid_aueryset().alias(date=TruncDate("create_time")).annotate(date=models.F("date")).filter(
            date__range=(self._today.replace(day=1),self._today)
        )
        pay_price__sum = qs.aggregate(models.Sum("pay_price"))["pay_price__sum"] or 0
        return pay_price__sum
    
    # 日环比
    def orders_amount_ratio(self):
        """ 今日销售总额环比 """
        today_amount = self.orders_today_amount()
        yesterday_amount = self.orders_yesterday_amount()
        if yesterday_amount == 0: return 0
        growth_rate = (today_amount - yesterday_amount) / yesterday_amount
        return round(growth_rate, 2) * 100

    def orders_today_count(self):
        """ 今日订单总数 """
        return self.orders_queryset().filter(create_time__date=self._today).count()
    
    def orders_yesterday_count(self):
        """ 昨日订单总数 """
        return self.orders_queryset().filter(create_time__date=self._yesterday).count()
    
    def orders_week_count(self):
        """ 本周订单总数 """
        qs = self.orders_queryset().alias(date=TruncDate("create_time")).annotate(date=models.F("date"))
        return qs.filter(date__range=(self._yesterday - timezone.timedelta(days=6), self._yesterday)).count()
    
    def orders_month_count(self):
        """ 本月订单总数 """
        qs = self.orders_queryset().alias(date=TruncDate("create_time")).annotate(date=models.F("date"))
        return qs.filter(date__range=(self._today.replace(day=1), self._today)).count()
    
    def orders_year_count(self):
        """ 本年订单总数 """
        qs = self.orders_queryset().alias(date=TruncDate("create_time")).annotate(date=models.F("date"))
        return qs.filter(date__range=(self._yesterday.replace(month=1, day=1), self._yesterday)).count()
    
    def orders_paid_count(self):
        """ 已支付订单总数 """
        return self.orders_paid_aueryset().count()
    
    # 日环比
    def orders_count_ratio(self):
        """ 今日订单总数环比 """
        today_count = self.orders_today_count()
        yesterday_count = self.orders_yesterday_count()
        if yesterday_count == 0: return 0
        growth_rate = (today_count - yesterday_count) / yesterday_count
        return round(growth_rate, 2) * 100

    # 订单图表数据
    def orders_chart_data(self):
        """ 订单图表数据 """
        qs = self.orders_paid_aueryset().alias(date=TruncDate("create_time")).annotate(date=models.F("date"))
        results = []
        for date in self.get_month_dates():
            obj = {"date": date.strftime('%m-%d')}
            pay_price__sum = qs.filter(date=date).aggregate(models.Sum("pay_price"))['pay_price__sum'] or 0
            obj["total"] = str(pay_price__sum)
            obj["count"] = qs.filter(date=date).count()
            results.append(obj)
        return results
    
    def get_30days_orders_chart(self):
        """ 当月订单数据图表 """
        datas = self.orders_chart_data()
        max_total = max(datas, key=lambda x: x['total'])['total']
        max_count = max(datas, key=lambda x: x['count'])['count']
        colors = ["#79AEC8", "#d14a61", "#675bba"]
        x_data = [item['date'] for item in datas]
        rainfall_capacity = [item['total'] for item in datas]
        average_temperature = [item['count'] for item in datas]
        bar = (
            Bar(init_opts=opts.InitOpts(
                    width="calc(100% - 290px);", 
                    height="350px", 
                    theme=ThemeType.WALDEN,
                    js_host="/static/core/js/"
                    # bg_color="#F8F8F8",
                )
            ).set_global_opts(
                title_opts=opts.TitleOpts(title="订单统计", pos_left="30"),
                tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
                toolbox_opts=opts.ToolboxOpts(is_show=True),
            )
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
                series_name="订单金额", y_axis=rainfall_capacity, yaxis_index=1, color=colors[0]
            )
            .extend_axis(
                yaxis=opts.AxisOpts(
                    name="金额",
                    type_="value",
                    min_=0,
                    max_=max_total,
                    position="right",
                    axisline_opts=opts.AxisLineOpts(
                        linestyle_opts=opts.LineStyleOpts(color=colors[1])
                    ),
                    axislabel_opts=opts.LabelOpts(formatter="{value}"),
                )
            )
            .extend_axis(
                yaxis=opts.AxisOpts(
                    type_="value",
                    name="数量",
                    min_=0,
                    max_=max_count,
                    position="left",
                    axisline_opts=opts.AxisLineOpts(
                        linestyle_opts=opts.LineStyleOpts(color=colors[2])
                    ),
                    axislabel_opts=opts.LabelOpts(formatter="{value} 单"),
                    splitline_opts=opts.SplitLineOpts(
                        is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
                    ),
                )
            )
        )

        line = (
            Line()
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
                series_name="订单数", y_axis=average_temperature, yaxis_index=2, color=colors[2]
            )
        )
        return bar.overlap(line).render_embed()