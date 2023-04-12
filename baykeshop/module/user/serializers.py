from rest_framework import serializers

from baykeshop.module.user.models import BaykeShopAddress


class BaykeShopAddressSerializer(serializers.ModelSerializer):
    
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = BaykeShopAddress
        # fields = "__all__"
        exclude = ('site',)