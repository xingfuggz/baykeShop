from decimal import Decimal
from django.core.cache import cache
from django.db.models.expressions import F

from baykeshop.module.product.models import BaykeProduct
from baykeshop.module.cart.models import BaykeShopingCart
from baykeshop.module.cart.serializers import (
    CartBaykeProductSerializer, CartBaykeShopingListSerializer
)
from baykeshop.module.order.models import BaykeOrderGoods


class BaseComputedPayMent:
        
    action = None
    model = None
    serializer_class = None
    
    def __init__(self, request, sku:int=None, num=1) -> None:
        self.actions = ['nowBuy', 'cartBuy']
        self.cache_cart = cache.get(f"{request.user.id}cartBuy")
        self.sku = sku
        self.num = num
        self.request = request
    
    @property
    def validate(self):
        is_pay = False
        if self.action == 'nowBuy' and isinstance(self.sku, int):
            is_pay = True
        elif self.action == 'cartBuy' and self.cache_cart:
            is_pay = True
        return is_pay
            
    def get_queryset(self):
        if self.validate:
            return self.model.objects.all()
        
    def get_serializer(self):
        return self.serializer_class(self.get_queryset(), many=True)
    
    def get_serializer_data(self):
        return self.get_serializer().data
        
    def total_price(self, price, num):
        return Decimal(price) * int(num)
    
    def get_context(self):
        context = self.get_serializer_data()
        for data in context:
            count = int(self.num) if self.action == 'nowBuy' else data.get('num', 1)
            price = data['price'] if self.action == 'nowBuy' else data['sku']['price']  
            if self.action == 'nowBuy':
                data['count'] = count
                data['totalPrice'] = self.total_price(price, count)
            elif self.action == 'cartBuy':
                data['sku']['count'] = count
                data['sku']['totalPrice'] = self.total_price(price, count)
        return context
    
    def get_skus(self):
        # 统一sku的格式
        skus = []
        if self.action == 'nowBuy':
            skus = self.get_context()
        elif self.action == 'cartBuy':
            for cart in self.get_context():
                skus.append(cart['sku'])
        return skus
    
    def get_freight(self):
        # 运费
        skus = self.get_skus()
        return sum([Decimal(sku['goods']['freight']) for sku in skus])
    
    def get_num(self):
        # 商品总数
        skus = self.get_skus()
        return sum([int(sku['count']) for sku in skus])
    
    def get_total(self):
        # 不含运费的总价
        skus = self.get_skus()
        return sum([Decimal(sku['totalPrice']) for sku in skus])
    
    def get_total_amount(self):
        # 含运费总价
        return self.get_total() + self.get_freight()
    
    def computed(self):
        return {
            'num': self.get_num(), 
            'total': self.get_total(), 
            'freight': self.get_freight(), 
            'total_amount': self.get_total_amount()
        }
    
    def save_order_goods(self, orderinfo):
        skus = self.get_skus()
        for sku in skus:
            product = BaykeProduct.objects.get(id=sku['id'])
            BaykeOrderGoods.objects.create(
                orderinfo=orderinfo, 
                title=sku['goods']['title'],
                options = sku['options'],
                price=sku['price'],
                content=sku['goods']['content'],
                count=sku['count'],
                product=product
            )
            # 减库存加销量
            product.stock = F('stock')-int(sku['count'])
            product.sales = F('sales')+int(sku['count'])
            product.save()
        return orderinfo
        

class NowBuyComputed(BaseComputedPayMent):
    """ 立即购买 """
    action = "nowBuy"
    model = BaykeProduct
    serializer_class = CartBaykeProductSerializer
    
    def get_queryset(self):
        return super().get_queryset().filter(id=int(self.sku))
    
    
class CartBuyComputed(BaseComputedPayMent):
    """ 购物车结算 """
    action = "cartBuy"
    model = BaykeShopingCart
    serializer_class = CartBaykeShopingListSerializer
    
    def get_queryset(self):
        carts_ids = [int(cart['id']) for cart in self.cache_cart['skus']]
        return super().get_queryset().filter(owner=self.request.user, id__in=carts_ids)
    

def computed_pay(request, action, sku, num):
    # 工厂函数
    pay = None
    if action == 'cartBuy':
        pay = CartBuyComputed(request)
    elif action == 'nowBuy':
        pay = NowBuyComputed(request, int(sku), int(num))
    return pay
