from django.core.cache import cache

from baykeshop.module.product.models import BaykeProduct
from baykeshop.module.cart.models import BaykeShopingCart
from baykeshop.module.cart.serializers import (
    CartBaykeProductSerializer, CartBaykeShopingListSerializer
)


class ComputedPayMent:
    
    def __init__(self, request) -> None:
        self.request = request
        self.query = self.request.query_params
        self.actions = ['nowBuy', 'cartBuy']
        self.action = None
        
    # def __call__(self, *args, **kwds):
    #     return self.get_serializer_data
    
    def get_cache_carts(self):
        return cache.get(f"{self.request.user}cartBuy")
    
    @property
    def get_action(self):
        if self.query and self.query.get('action') in self.actions:
            self.action = self.query.get('action')
        return self.action
    
    @property    
    def validate(self):
        # 验证是否为立即购买或购物车结算，
        # 如果不是，阻止一切运行，防止页面报错
        is_pay = False
        action = self.get_action
        query = self.query
        if query.get('sku') and query.get('num') and action:
            is_pay = True
        elif self.get_cache_carts() and action:
            is_pay = True
        return is_pay
    
    @property
    def query_validate_data(self):
        if self.validate:
            return self.query.dict()
    
    def get_queryset(self):
        """ 根据传递的操作参数返回对应的queryset """
        queryset = None
        query = self.query_validate_data
        if self.get_action == 'nowBuy':
            queryset = BaykeProduct.objects.filter(id=int(query.get('sku')))
        elif self.get_action == 'cartBuy':
            cart_ids = [cart['id'] for cart in self.get_cache_carts()]
            queryset = BaykeShopingCart.objects.filter(id=cart_ids)
        return queryset
    
    def get_serializer_class(self):
        # 根据验证信息返回对应的序列化类
        serializer_class = None
        if self.get_action == 'nowBuy':
            serializer_class = CartBaykeProductSerializer
        elif self.get_action == 'cartBuy':
            serializer_class = CartBaykeShopingListSerializer
        return serializer_class
    
    @property
    def get_serializer(self):
        # 根据传入的渠道返回对应的serializer
        serializer = None
        serializer_class = self.get_serializer_class()
        if self.get_action == 'nowBuy':
            serializer = serializer_class(CartBaykeProductSerializer(self.get_queryset()), many=True)
        elif self.get_action == 'cartBuy':
            serializer = serializer_class(CartBaykeShopingListSerializer(self.get_queryset()), many=True)
        print(self.get_action)
        print(serializer)
        return serializer
    
    def get_serializer_data(self):
        data = self.get_serializer
        print(data)
        return data