from rest_framework import serializers
from django.db.utils import IntegrityError
from rest_framework.validators import UniqueTogetherValidator

from baykeshop.module.user.models import BaykeShopAddress


class BaykeShopAddressSerializer(serializers.ModelSerializer):
    
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = BaykeShopAddress
        exclude = ('site',)
