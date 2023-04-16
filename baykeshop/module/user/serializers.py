from django.contrib.auth import get_user_model
from rest_framework import serializers

from baykeshop.conf import bayke_settings
from baykeshop.module.user.models import BaykeShopAddress, BaykeUserInfo, BaykeUserBalanceLog


User = get_user_model()


class BaykeShopAddressSerializer(serializers.ModelSerializer):
    
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = BaykeShopAddress
        exclude = ('site',)


class BaykeUserBalanceLogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BaykeUserBalanceLog
        fields = "__all__"


class BaykeUserInfoSerializer(serializers.ModelSerializer):
    
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    balance = serializers.ReadOnlyField()
    
    class Meta:
        model = BaykeUserInfo
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    
    baykeuserinfo = BaykeUserInfoSerializer(many=False)
    username = serializers.ReadOnlyField()
    baykeuserbalancelog_set = BaykeUserBalanceLogSerializer(many=True, read_only=True)
  
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'baykeuserinfo', 'baykeuserbalancelog_set')
        
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        try:
            BaykeUserInfo.objects.filter(owner=instance).update(**validated_data['baykeuserinfo'])
        except KeyError:
            pass
        instance.save()
        return instance
    
    def validate_baykeuserinfo(self, data):
        try:
            import re
            phone = data['phone']
            reg = re.compile(bayke_settings.PHONE_REGX)
            if not reg.search(phone):
                raise serializers.ValidationError("手机号格式有误！")
        except KeyError:
            pass
        return data
    
    # def get_balancelog(self, obj):
    #     print(obj)
    #     return 'asdas'