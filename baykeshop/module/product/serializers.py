from rest_framework import serializers

from baykeshop.models import product


class BaykeCategorySetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = product.BaykeCategory
        fields = "__all__"


class BaykeCategorySerializer(serializers.ModelSerializer):
    
    # children = serializers.SerializerMethodField()
    
    class Meta:
        model = product.BaykeCategory
        fields = "__all__"
        
    # def get_children(self, obj):
    #     return BaykeCategorySetSerializer(obj.baykecategory_set.all(), many=True).data
        
    