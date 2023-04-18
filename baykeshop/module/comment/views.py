from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication


from rest_framework.renderers import JSONRenderer
from baykeshop.public.renderers import TemplateHTMLRenderer
from baykeshop.module.comment.page import CommentsPageNumberPagination
from baykeshop.module.comment.models import BaykeOrderInfoComments


class BaykeOrderInfoCommentsViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    # pagination_class = CommentsPageNumberPagination
    
    def get_queryset(self):
        return BaykeOrderInfoComments.objects.filter(owner=self.request.user)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    
