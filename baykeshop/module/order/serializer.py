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