from django.core.files.storage import default_storage
from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

class UploadImageView(View):
    """
    上传文件
    """
    def _validate(self, request):
        # 验证权限
        is_perm = False
        if request.user.is_authenticated and request.user.has_perm('core.add_uploadimage'):
            is_perm = True
        return is_perm

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        if not self._validate(request):
            return JsonResponse({'error': '权限不足'})
        file = request.FILES.get('file')
        if file:
            file_name = default_storage.save(file.name, file)
            return JsonResponse({'code': 200, 'url': default_storage.url(file_name)})
        return JsonResponse({'code': 400 ,'msg': '文件上传失败'})