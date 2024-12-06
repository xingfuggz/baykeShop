#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :echarts.py
@说明    :分析图表
@时间    :2024/12/06 22:47:24
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''


from django.db import models
from django.utils.translation import gettext_lazy as _

from pyecharts.charts import Bar, Line, Pie
from pyecharts import options as opts
from pyecharts.globals import ThemeType

from baykeshop.db.analysis import (
    OrderAnalysisService,
    VisitAnalysisService,
    UserAnalysisService,
)

order_analysis_service = OrderAnalysisService()
visit_analysis_service = VisitAnalysisService()
user_analysis_service = UserAnalysisService()


def orders_chart():
    """订单统计图表"""
    data = order_analysis_service.get_month_sales_data_dict(format="%m-%d")
    x_data = list(data.keys())
    y_data = list(data.values())
    month_counts = order_analysis_service.get_last_month_data()
    colors = ["#79AEC8", "#d14a61", "#675bba"]
    bar = (
        Bar(
            init_opts=opts.InitOpts(
                width="calc(100% - 290px);",
                height="350px",
                theme=ThemeType.WALDEN,
                js_host="/static/baykeshop/js/",
                # bg_color="#F8F8F8",
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="订单统计", pos_left="30"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
        )
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            series_name="订单金额", y_axis=y_data, yaxis_index=1, color=colors[0]
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                name="金额",
                type_="value",
                min_=0,
                max_=max(y_data),
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
                max_=max(month_counts),
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
            series_name="订单数", y_axis=month_counts, yaxis_index=2, color=colors[2]
        )
    )
    return bar.overlap(line).render_embed()


def users_chart():
    """用户统计图表"""
    datas = user_analysis_service.get_last_week_data_dict("%m-%d")
    x_data = list(datas.keys())
    y_data = list(datas.values())
    c = (
        Line(
            init_opts=opts.InitOpts(
                width="calc(100% - 100px);",
                # width="100%",
                height="300px",
                theme=ThemeType.WALDEN,
                js_host="/static/baykeshop/js/",
                # bg_color="#F8F8F8",
            )
        )
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


def user_pie_chart():
    """用户统计图表"""
    # 本月新增用户数
    user_datas = user_analysis_service.get_queryset().filter(
        date__range=(user_analysis_service._last_month, user_analysis_service._today)
    )
    # 未消费用户数
    no_order_user_datas = user_datas.filter(baykeshoporders__isnull=True)
    # 消费1次以上用户数
    one_order_user_datas = (
        user_datas.filter(baykeshoporders__isnull=False)
        .annotate(count=models.Count("id"))
        .filter(count__gt=1)
    )
    # 排除本月新增的用户
    exclude_month_users = (
        user_analysis_service.get_queryset()
        .exclude(
            date__range=(
                user_analysis_service._last_month,
                user_analysis_service._today,
            )
        )
        .filter(baykeshoporders__isnull=False)
    )
    # 回流用户数,获取过去消费的用户数据和本月消费的用户数据做交集
    reflux_users = exclude_month_users.values_list("id", flat=True).intersection(
        one_order_user_datas.values_list("id", flat=True)
    )
    results = [
        ["留存", len(set(reflux_users))],
        ["消费1次以上", one_order_user_datas.count()],
        ["未消费", no_order_user_datas.count()],
        ["新增", user_analysis_service.last_month_count()],
    ]

    c = (
        Pie(
            init_opts=opts.InitOpts(
                width="600px",
                # width="100%",
                height="300px",
                theme=ThemeType.WALDEN,
                js_host="/static/baykeshop/js/",
                # bg_color="#F8F8F8",
            )
        )
        .add(
            "本月用户消费统计",
            results,
            center=["40%", "55%"],
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=_("当月购买用户统计")),
            legend_opts=opts.LegendOpts(pos_left="70%"),
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    ).render_embed()
    return c
