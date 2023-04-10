from rest_framework import serializers

from baykeshop.models import product
from baykeshop.public.serializers import BaykeGoodsSerializer


class BaykeCategorySetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = product.BaykeCategory
        fields = "__all__"


class BaykeCategorySerializer(serializers.ModelSerializer):
     
    class Meta:
        model = product.BaykeCategory
        fields = "__all__"
        
        

class BaykeGoodsDetailSerializer(BaykeGoodsSerializer):
    
    class Meta:
        model = product.BaykeGoods
        fields = "__all__"