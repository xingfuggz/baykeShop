from rest_framework import serializers

from baykeshop.models import public
from baykeshop.models import product


class BaykeBannerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = public.BaykeBanner
        fields = "__all__"
    
    
class BaykeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = product.BaykeProduct
        fields = "__all__"


class BaykeGoodsSerializer(serializers.ModelSerializer):
    
    baykeproduct_set = BaykeProductSerializer(many=True)
    
    class Meta:
        model = product.BaykeGoods
        fields = "__all__"


class HomeBaykeCategorySerializer(serializers.ModelSerializer):
    
    products = serializers.SerializerMethodField()

    class Meta:
        model = product.BaykeCategory
        fields = "__all__"
    
    def get_products(self, obj):
        return BaykeGoodsSerializer(product.BaykeGoods.objects.filter(
            categorys__in=obj.baykecategory_set.all()), many=True).data
        
        
        