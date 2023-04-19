from rest_framework import serializers

from baykeshop.module.comment.models import BaykeOrderInfoComments
from baykeshop.module.user.serializers import UserSerializer



class BaykeOrderInfoCommentsSerializer(serializers.ModelSerializer):
    
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    userinfo = serializers.SerializerMethodField()
    
    class Meta:
        model = BaykeOrderInfoComments
        fields = "__all__"
    
    def get_userinfo(self, obj):
        return UserSerializer(obj.owner, many=False).data