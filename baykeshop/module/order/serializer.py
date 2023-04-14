from django.utils import timezone
from rest_framework import serializers

from baykeshop.module.cart.serializers import CartBaykeProductSerializer
from baykeshop.module.order.models import BaykeOrderInfo, BaykeOrderGoods
from baykeshop.module.payment.computed import computed_pay


class BaykeOrderGoodsSerializer(serializers.ModelSerializer):
    """ 订单商品序列化 """
    product = CartBaykeProductSerializer(many=False, read_only=True)
    
    class Meta:
        model = BaykeOrderGoods
        fields = "__all__"


class BaykeOrderInfoSerializer(serializers.ModelSerializer):
    """ 订单序列化 """
    
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    baykeordergoods_set = BaykeOrderGoodsSerializer(read_only=True, many=True)
    pay_methods = serializers.SerializerMethodField()
    
    class Meta:
        model = BaykeOrderInfo
        fields = "__all__"
        
    def generate_order_sn(self):
        # 当前时间 + userid + 随机数
        from random import Random
        random_ins = Random()
        order_sn = "{time_str}{user_id}{ranstr}".format(
            time_str = timezone.now().strftime("%Y%m%d%H%M%S"),
            user_id = self.context["request"].user.id,
            ranstr = random_ins.randint(10, 99))
        return order_sn
    
    def validate(self, attrs):
        # 设置order_sn的值
        attrs["order_sn"] = self.generate_order_sn()
        return attrs
    
    def get_pay_methods(self, obj):
        pay_methods = BaykeOrderInfo.get_pay_method()  
        pay_list = [
            { 
                'value': 1,
                'name': pay_methods[1],
                'icon': "/static/baykeshop/img/hdpay.svg",
                'is_default': False,
            },
            { 
                'value': 2,
                'name': pay_methods[2],
                'icon': "/static/baykeshop/img/alipay.svg",
                'is_default': True,
            },
            { 
                'value': 3,
                'name': pay_methods[3],
                'icon': "/static/baykeshop/img/wxpay.svg",
                'is_default': False,
            },
            { 
                'value': 4,
                'name': pay_methods[4],
                'icon': "/static/baykeshop/img/ye.svg",
                'is_default': False,
            }
        ]
        return pay_list