from rest_framework import serializers

from baykeshop.models import product


class HomeBaykeCategorySerializer(serializers.ModelSerializer):
    
    products = serializers.SerializerMethodField()
    
    class Meta:
        model = product.BaykeCategory
        fields = "__all__"
    
    def get_products(self, obj):
        if obj.parent is None:
            return list(
                product.BaykeGoods.objects.filter(
                    categorys__in=obj.baykecategory_set.all()
                ).distinct().values()
            )