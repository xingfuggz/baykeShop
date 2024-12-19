from django.db.models import Sum, F, Q
from django.db.models.functions import TruncDate
from django.contrib.auth import get_user_model
from django.utils import timezone
from baykeshop.contrib.system.models import Visit
from baykeshop.contrib.shop.models import BaykeShopOrders

User = get_user_model()


class DateService:
    """分析服务"""

    @property
    def _today(self):
        """今天"""
        return timezone.now().date()

    @property
    def _yesterday(self):
        """昨天"""
        return self._today - timezone.timedelta(days=1)

    @property
    def _last_week(self):  # 上周
        """上周"""
        return self._today - timezone.timedelta(days=7)

    @property
    def _last_month(self):  # 上月
        """上月"""
        return self._today - timezone.timedelta(days=30)

    # 获取最近一周的日期
    def get_last_week_date(self):
        """获取最近一周的日期"""
        return [self._last_week + timezone.timedelta(days=i) for i in range(7)]

    def get_last_month_date(self):
        """获取最近一月的日期"""
        return [self._last_month + timezone.timedelta(days=i) for i in range(30)]


class AnalysisService(DateService):
    """分析服务"""

    date_field = "created_time"
    queryset = None

    def __init__(self, request=None):
        super().__init__()
        self.request = request

    @property
    def _date_field(self):  # 默认时间字段
        """时间字段"""
        return self.date_field

    def get_queryset(self):
        """获取查询集"""
        if self.queryset is None:  # 缓存
            return User.objects.none()
        return self.queryset.annotate(date=TruncDate(self._date_field))

    def count(self):
        """总数"""
        queryset = self.get_queryset()
        if queryset.exists():  # 存在则取最后一条
            return queryset.count()
        return 0

    def today_count(self):
        """今日总数"""
        queryset = self.get_queryset().filter(date=self._today)
        if queryset.exists():  # 存在则取最后一条
            return queryset.count()
        return 0

    def yesterday_count(self):
        """昨日总数"""
        queryset = self.get_queryset().filter(date=self._yesterday)
        if queryset.exists():  # 存在则取最后一条
            return queryset.count()
        return 0

    def last_week_count(self):
        """最近一周总数"""
        queryset = self.get_queryset().filter(
            date__range=(self._last_week, self._today)
        )
        if queryset.exists():
            return queryset.count()
        return 0

    def last_month_count(self):
        """最近一月总数"""
        queryset = self.get_queryset().filter(
            date__range=(self._last_month, self._today)
        )
        if queryset.exists():
            return queryset.count()
        return 0

    def get_last_week_data(self):
        """最近一周数据"""
        return [
            self.get_queryset().filter(date=date).count()
            for date in self.get_last_week_date()
        ]

    def get_last_month_data(self):
        """最近一月数据"""
        return [
            self.get_queryset().filter(date=date).count()
            for date in self.get_last_month_date()
        ]

    def get_last_week_data_dict(self, format=None):
        """最近一周数据字典
        @param format: 日期格式 %Y-%m-%d
        """
        if format:  # 获取日期字符串
            return {
                date.strftime(format): count
                for date, count in zip(
                    self.get_last_week_date(), self.get_last_week_data()
                )
            }
        return dict(zip(self.get_last_week_date(), self.get_last_week_data()))

    def get_last_month_data_dict(self, format=None):
        """最近一月数据字典"""
        if format:  # 获取日期字符串
            return {
                date.strftime(format): count
                for date, count in zip(
                    self.get_last_month_date(), self.get_last_month_data()
                )
            }
        return dict(zip(self.get_last_month_date(), self.get_last_month_data()))

    # 日环比率
    def get_ratio(self):
        """日环比率"""
        if self.yesterday_count() == 0:
            return 0
        return round(
            (self.today_count() - self.yesterday_count())
            / self.yesterday_count()
            * 100,
            2,
        )

    def get_data(self, format=None):
        """获取数据"""
        return {
            "count": self.count(),
            "today_count": self.today_count(),
            "yesterday_count": self.yesterday_count(),
            "last_week_count": self.last_week_count(),
            "last_month_count": self.last_month_count(),
            # 'last_week_data': self.get_last_week_data(),
            # 'last_month_data': self.get_last_month_data(),
            "last_week_data_dict": self.get_last_week_data_dict(format),
            "last_month_data_dict": self.get_last_month_data_dict(format),
            "ratio": self.get_ratio(),
        }


class UserAnalysisService(AnalysisService):
    """用户分析服务"""

    # queryset = User.objects.filter(is_staff=False)
    queryset = User.objects.all()
    date_field = "date_joined"


class OrderAnalysisService(AnalysisService):
    """订单分析服务"""

    def __init__(
        self,
        model=None,
        request=None,
    ):
        super().__init__(request)
        self.model = model or BaykeShopOrders
        self.queryset = self.model.objects.all()

    def get_queryset(self):
        """获取查询集"""
        return (
            super()
            .get_queryset()
            .exclude(
                Q(status=self.model.OrderStatus.UNPAID)
                | Q(status=self.model.OrderStatus.EXPIRED)
                | Q(status=self.model.OrderStatus.REFUNDED)
            )
        )

    # 昨日销售额
    def yesterday_sales(self):
        """昨日销售额"""
        return (
            self.get_queryset()
            .filter(date=self._yesterday)
            .aggregate(sales=Sum("pay_price"))["sales"]
            or 0
        )

    # 今日销售额
    def today_sales(self):
        """今日销售额"""
        return (
            self.get_queryset()
            .filter(date=self._today)
            .aggregate(sales=Sum("pay_price"))["sales"]
            or 0
        )

    # 本月销售额
    def last_month_sales(self):
        """本月销售额"""
        return (
            self.get_queryset()
            .filter(date__range=(self._last_month, self._today))
            .aggregate(sales=Sum("pay_price"))["sales"]
            or 0
        )

    def get_week_sales_data(self):
        """销售额数据"""
        return [
            self.get_queryset()
            .filter(date=date)
            .aggregate(sales=Sum("pay_price"))["sales"]
            or 0
            for date in self.get_last_week_date()
        ]

    def get_week_sales_data_dict(self, format=None):
        """销售额数据字典"""
        if format:  # 获取日期字符串
            return {
                date.strftime(format): count
                for date, count in zip(
                    self.get_last_week_date(), self.get_week_sales_data()
                )
            }
        return dict(zip(self.get_last_week_date(), self.get_week_sales_data()))

    def get_month_sales_data(self):
        """本月销售额数据"""
        return [
            self.get_queryset()
            .filter(date=date)
            .aggregate(sales=Sum("pay_price"))["sales"]
            or 0
            for date in self.get_last_month_date()
        ]

    def get_month_sales_data_dict(self, format=None):
        """本月销售额数据字典"""
        if format:  # 获取日期字符串
            return {
                date.strftime(format): count
                for date, count in zip(
                    self.get_last_month_date(), self.get_month_sales_data()
                )
            }
        return dict(zip(self.get_last_month_date(), self.get_month_sales_data()))

    def get_sales_ratio(self):
        """销售额环比率"""
        if self.yesterday_sales() == 0:
            return 0
        return round(
            (self.today_sales() - self.yesterday_sales())
            / self.yesterday_sales()
            * 100,
            2,
        )

    def get_sales_data(self, format=None):
        return {
            "yesterday_sales": self.yesterday_sales(),
            "today_sales": self.today_sales(),
            "last_month_sales": self.last_month_sales(),
            # 'week_sales_data': self.get_week_sales_data(),
            "week_sales_data_dict": self.get_week_sales_data_dict(format),
            # 'month_sales_data': self.get_month_sales_data(),
            "month_sales_data_dict": self.get_month_sales_data_dict(format),
            "sales_ratio": self.get_sales_ratio(),
        }


class VisitAnalysisService(AnalysisService):
    """访问分析服务"""

    def get_queryset(self):
        return Visit.objects.all()

    def _count(self):
        """总量计算"""
        datas = self.get_queryset().aggregate(count_uv=Sum("uv"), count_pv=Sum("pv"))
        return self._to_int_dict(datas)

    def count(self):
        """总访问量"""
        return self._count()

    def today_count(self):
        """今日访问量"""
        queryset = self.get_queryset().filter(date=self._today)
        datas = queryset.aggregate(count_pv=Sum("pv"), count_uv=Sum("uv"))
        return self._to_int_dict(datas)

    def yesterday_count(self):
        """昨日访问量"""
        queryset = self.get_queryset().filter(date=self._yesterday)
        datas = queryset.aggregate(count_pv=Sum("pv"), count_uv=Sum("uv"))
        return self._to_int_dict(datas)

    def last_week_count(self):  # 获取上周访问量
        """上周访问量"""
        queryset = self.get_queryset().filter(
            date__range=(self._last_week, self._yesterday)
        )
        datas = queryset.aggregate(count_pv=Sum("pv"), count_uv=Sum("uv"))
        return self._to_int_dict(datas)

    def last_month_count(self):  # 获取上月访问量
        """上月访问量"""
        queryset = self.get_queryset().filter(
            date__range=(self._last_month, self._yesterday)
        )
        datas = queryset.aggregate(count_pv=Sum("pv"), count_uv=Sum("uv"))
        return self._to_int_dict(datas)

    def get_last_week_data(self):
        """最近一周的pv及uv数据"""
        return [
            self._to_int_dict(
                self.get_queryset()
                .filter(date=date)
                .aggregate(count_pv=Sum("pv"), count_uv=Sum("uv"))
            )
            for date in self.get_last_week_date()
        ]

    def get_last_month_data(self):
        """最近一月的pv及uv数据"""
        return [
            self._to_int_dict(
                self.get_queryset()
                .filter(date=date)
                .aggregate(count_pv=Sum("pv"), count_uv=Sum("uv"))
            )
            for date in self.get_last_month_date()
        ]

    def _uv_ration(self, field_name="count_uv"):
        if self.yesterday_count()[field_name] == 0:
            return 0
        ration = round(
            (self.today_count()[field_name] - self.yesterday_count()[field_name])
            / self.yesterday_count()[field_name]
            * 100,
            2,
        )
        return ration

    def _pv_ration(self, field_name="count_pv"):
        if self.yesterday_count()[field_name] == 0:
            return 0
        ration = round(
            (self.today_count()[field_name] - self.yesterday_count()[field_name])
            / self.yesterday_count()[field_name]
            * 100,
            2,
        )
        return ration

    def get_ratio(self):
        """获取比率"""
        return {"pv": self._pv_ration(), "uv": self._uv_ration()}

    # None转换为0
    def _to_int(self, value):
        return value if value else 0

    # 字典中value为None转换为0
    def _to_int_dict(self, data):
        return {k: self._to_int(v) for k, v in data.items()}
