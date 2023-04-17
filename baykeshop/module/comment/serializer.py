from rest_framework import serializers

from baykeshop.module.comment.models import BaykeOrderInfoComments


class BaykeOrderInfoCommentsSerializer(serializers.ModelSerializer):
    
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = BaykeOrderInfoComments
        fields = "__all__"