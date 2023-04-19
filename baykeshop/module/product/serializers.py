from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from baykeshop.models import product
from baykeshop.public.serializers import BaykeGoodsSerializer
from baykeshop.module.order.models import BaykeOrderGoods
from baykeshop.module.comment.models import BaykeOrderInfoComments
from baykeshop.module.comment.serializer import BaykeOrderInfoCommentsSerializer


class BaykeCategorySerializer(serializers.ModelSerializer):
    """ 商品分类 """
    class Meta:
        model = product.BaykeCategory
        fields = "__all__"


class BaykeSpecOptionsSerializer(serializers.ModelSerializer):
    """ 商品规格值 """
    
    spec = serializers.StringRelatedField()
    
    class Meta:
        model = product.BaykeSpecOptions
        fields = "__all__"


class BaykeSpecSerializer(serializers.ModelSerializer):
    """ 商品规格 """
    baykespecoptions_set = BaykeSpecOptionsSerializer(many=True)
    
    class Meta:
        model = product.BaykeSpec
        fields = "__all__"
  
  
class BaykeProductDetailSerializer(serializers.ModelSerializer):
    """ 商品规格 """
    options = BaykeSpecOptionsSerializer(many=True)
    
    class Meta:
        model = product.BaykeProduct
        fields = "__all__"      


class BaykeGoodsBannersSerializer(serializers.ModelSerializer):
    """ 轮播图序列化 """
    class Meta:
        model = product.BaykeGoodsBanners
        fields = "__all__"
    

class BaykeGoodsDetailSerializer(serializers.ModelSerializer):
    """ 商品详情页序列化 """
    
    baykeproduct_set = BaykeProductDetailSerializer(product.BaykeProduct.objects.filter(is_release=True), many=True)
    baykegoodsbanners_set = BaykeGoodsBannersSerializer(many=True)
    specs = serializers.SerializerMethodField()
    hot_goods = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = product.BaykeGoods
        fields = "__all__"
        
    def get_specs(self, obj):
        # 序列化规格
        spec_ids = obj.baykeproduct_set.filter(is_release=True).values_list('options__spec__id', flat=True)
        specs = BaykeSpecSerializer(product.BaykeSpec.objects.filter(id__in=list(set(spec_ids))), many=True)
        return specs.data
    
    def get_hot_goods(self, obj):
        hots = []
        hot_goods = BaykeGoodsSerializer(product.BaykeGoods.objects.order_by('-baykeproduct__sales'), many=True)
        for hot in hot_goods.data:
            if hot not in hots:
                hots.append(hot)
        return hots[:5]
    
    def get_comments(self, obj):
        """ 评价列表 """
        content_type = ContentType.objects.get_for_model(BaykeOrderGoods)
        product_ids = obj.baykeproduct_set.filter(is_release=True).values_list('id', flat=True)
        order_goods_ids = BaykeOrderGoods.objects.filter(product__id__in=list(product_ids)).values_list('id', flat=True)
        comments = BaykeOrderInfoComments.objects.filter(content_type=content_type, object_id__in=list(order_goods_ids))
        return BaykeOrderInfoCommentsSerializer(comments, many=True).data
    