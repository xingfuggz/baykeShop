from rest_framework import serializers

from baykeshop.models import product


class BaykeCategorySerializer(serializers.ModelSerializer):
    
    # id = serializers.IntegerField(read_only=True)
    # name = serializers.CharField(max_length=50)
    # icon = serializers.CharField(max_length=50, requirend=False, default=False)
    # desc = serializers.CharField(max_length=150, requirend=False, default=False)
    # keywords = serializers.CharField(max_length=150, requirend=False, default=False)
    # parent = serializers.PrimaryKeyRelatedField()
    
    class Meta:
        model = product.BaykeCategory
        fields = "__all__"
    
    