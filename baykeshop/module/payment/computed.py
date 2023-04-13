from decimal import Decimal
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
    
    def get_cache_carts(self):
        return cache.get(f"{self.request.user.id}cartBuy")
    
    @property    
    def validate(self):
        # 验证是否为立即购买或购物车结算，
        # 如果不是，阻止一切运行，防止页面报错
        is_pay = False
        action = self.query.get('action')
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
        if self.query.get('action') == 'nowBuy':
            queryset = BaykeProduct.objects.filter(id=int(query.get('sku')))
        elif self.query.get('action') == 'cartBuy':
            cart_ids = [cart['id'] for cart in self.get_cache_carts()['skus']]
            queryset = BaykeShopingCart.objects.filter(id__in=cart_ids)    
        return queryset
    
    def get_serializer_class(self):
        # 根据验证信息返回对应的序列化类
        serializer_class = None
        if self.query.get('action') == 'nowBuy':
            serializer_class = CartBaykeProductSerializer(self.get_queryset(), many=True)
        elif self.query.get('action') == 'cartBuy':
            serializer_class = CartBaykeShopingListSerializer(self.get_queryset(), many=True)
        return serializer_class
    
    def get_context(self):
        context = {}
        if self.get_serializer_class():
            context = self.get_serializer_class().data
            if self.query.get('action') == 'nowBuy':
                context[0]['totalPrice'] = self.total_price(context[0]['price'], self.query.get('num', 1))
                context[0]['count'] = self.query.get('num', 1)
            elif self.query.get('action') == 'cartBuy':
                for cart in context:
                    cart['sku']['totalPrice'] = self.total_price(cart['sku']['price'], cart.get('num', 1))
                    cart['sku']['count'] = cart.get('num', 1)
        return context
    
    def total_price(self, price, num):
        # 计算价格
        return Decimal(price) * int(num)

    @property
    def computed(self):
        # 计算
        computed_dict = {'num': 0, 'total': 0, 'freight': 0, 'total_amount': 0}
        if self.query.get('action') == 'nowBuy':
            computed_dict['num'] = int(self.query.get('num'))
            computed_dict['total'] = self.total_price(self.get_context()[0]['price'], int(self.query.get('num')))
            computed_dict['freight'] = Decimal(self.get_context()[0]['goods']['freight'])
        elif self.query.get('action') == 'cartBuy':
            for cart in self.get_context():
                computed_dict['num'] += int(cart.get('num', 1))
                computed_dict['total'] += self.total_price(cart['sku']['price'], cart.get('num', 1))
                computed_dict['freight'] += Decimal(cart['sku']['goods']['freight'])
        computed_dict['total_amount'] = computed_dict['total'] + computed_dict['freight']
        return computed_dict
    
    def get_skus(self):
        # 使商品结构保持一致
        skus = []
        if self.query.get('action') == 'nowBuy':
            skus = self.get_context()
        elif self.query.get('action') == 'cartBuy':
            for cart in self.get_context():
                skus.append(cart['sku'])
        return skus