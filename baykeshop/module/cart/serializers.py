from rest_framework import serializers

from baykeshop.models import cart, product
from baykeshop.module.product.serializers import BaykeProductDetailSerializer


class BaykeShopingCartSerializer(serializers.ModelSerializer):

    owner = serializers.CurrentUserDefault()
    
    class Meta:
        model = cart.BaykeShopingCart
        fields = "__all__"


class CartBaykeGoodsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = product.BaykeGoods
        fields = "__all__"


class CartBaykeProductSerializer(BaykeProductDetailSerializer):
    
    goods = CartBaykeGoodsSerializer(read_only=True)
    
    class Meta:
        model = product.BaykeProduct
        fields = "__all__"   

    
class CartBaykeShopingListSerializer(serializers.ModelSerializer):
    """ cart list 视图专用序列化 """
    sku = CartBaykeProductSerializer(read_only=True)
    
    class Meta:
        model = cart.BaykeShopingCart
        fields = "__all__"