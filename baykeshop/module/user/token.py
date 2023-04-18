from django.contrib.auth import authenticate

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from baykeshop.module.user.serializers import UserSerializer


def get_tokens_for_user(user):
    """ 手动获取令牌 """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class BaykeTokenObtainPairSerializer(TokenObtainPairSerializer):  
    
    def validate(self, attrs):
        return super().validate(attrs)
    

class BaykeTokenObtainPairView(TokenObtainPairView):
    
    _serializer_class = "baykeshop.module.user.token.BaykeTokenObtainPairSerializer"
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        try:
            user = authenticate(username=request.data['username'], password=request.data['password'])
            if user is not None:
                response.data['userinfo'] = UserSerializer(user, many=False).data
        except KeyError:
            pass    
        return response