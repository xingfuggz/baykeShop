from django.http.response import JsonResponse
from django.views.generic import View

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from baykeshop.models import public
from baykeshop.models import product
from baykeshop.public.serializers import (
    HomeBaykeCategorySerializer, BaykeBannerSerializer
)
from baykeshop.conf import bayke_settings


class HomeView(GenericAPIView):
    """ 首页 """
    queryset = product.BaykeCategory.objects.filter(parent__isnull=True, is_nav=True)
    serializer_class = HomeBaykeCategorySerializer
    renderer_classes = (TemplateHTMLRenderer, JSONRenderer)
    authentication_classes = (SessionAuthentication, JWTAuthentication)
    
    def get(self, request):
        datas = {
            "cates": self.get_serializer().data,
            "banners": self.get_banners_serializer().data
        }
        return Response(datas, template_name="baykeshop/index.html")
    
    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(self.get_queryset(), many=True)
    
    def get_banners_serializer(self, *args, **kwargs):
        return BaykeBannerSerializer(public.BaykeBanner.objects.all(), many=True)
        

def has_upload_perm(request, perm_codename=None):
    # 权限判断方法
    perms = [
        request.user.is_authenticated,
        request.user.is_active,
        request.user.is_staff,
        request.user.has_perm(f'baykeshop.{perm_codename}') if perm_codename else True
    ]
    return False if not all(perms) else True

    
class TinymceUploadImg(View):
    """ tinymce 编辑器上传图片 """
    from django.views.decorators.csrf import csrf_exempt
    from django.utils.decorators import method_decorator
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        from baykeshop.public.models import BaykeUpload
        if not has_upload_perm(request, 'add_baykeupload'):
            return JsonResponse({"message": "无权限！"}, status=400)
        if request.FILES:
            from baykeshop.public.utils import add_upload_file 
            file_name = add_upload_file(request.FILES['file'])
            if file_name:
                baykeupload = BaykeUpload(img=f"{bayke_settings.FILE_PATH}{file_name}")
                baykeupload.save()
                return JsonResponse({'code': 'ok', 'location':f'{baykeupload.img.url}'})
            else:
                return JsonResponse({'code': 'err', 'message': 'error' })
        else:
            return JsonResponse({'code': 'err', 'message': 'qingxuanze' })
