from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from baykeshop.contrib.shop.models import BaykeShopOrdersComment, BaykeShopOrders


class BaykeShopOrdersCommentSerializer(serializers.ModelSerializer):
    """ 订单评论序列化器 """
    class Meta:
        model = BaykeShopOrdersComment
        fields = ('order', 'content', 'score')

    def validate_order(self, value):
        """ 验证订单 """
        request = self.context.get('request')
        if not (value.order.user == request.user):
            messages.error(request, _('订单与当前用户不匹配'))
            raise serializers.ValidationError(_('订单与当前用户不匹配'))

        if value.is_comment:
            messages.error(request, _('订单已评论, 请勿重复评论'))
            raise serializers.ValidationError(_('订单已评论, 请勿重复评论'))
        return value
    
    def create(self, validated_data):
        """ 创建评论 """
        instance = super().create(validated_data)
        instance.order.is_comment = True
        instance.order.status = BaykeShopOrders.OrderStatus.DONE
        instance.order.save()
        messages.success(self.context.get('request'), _('评论成功'))
        return instance
    