import json

from django.core import serializers
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse


from .models import BaykeGalleryCategory, BaykeGallery


class BaykeGalleryCategoryListView(LoginRequiredMixin, View):
    """图库分类列表"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'code': 403, 'msg': '请先登录'}, json_dumps_params={'ensure_ascii': False})
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        categories = BaykeGalleryCategory.objects.all()
        data = serializers.serialize('json', categories)
        data = json.loads(data)
        for item in data:
            item['category_url'] = reverse('gallery:category-detail', kwargs={'category_id': item['pk']})
        return JsonResponse({'code': 200, 'data': data}, json_dumps_params={'ensure_ascii': False})
    

class BaykeGalleryCategoryDetailView(LoginRequiredMixin, View):
    """图库分类详情"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'code': 403, 'msg': '请先登录'}, json_dumps_params={'ensure_ascii': False})
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        category_id = kwargs.get('category_id')
        category = BaykeGalleryCategory.objects.filter(id=category_id)
        if not category.exists():
            return JsonResponse({'code': 404, 'msg': '分类不存在'}, json_dumps_params={'ensure_ascii': False})
        gallery_queryset = BaykeGallery.objects.filter(category=category.first())
        data = serializers.serialize('json', gallery_queryset)
        data = json.loads(data)
        return JsonResponse({'code': 200, 'data': data}, json_dumps_params={'ensure_ascii': False})


class BaykeGalleryListView(LoginRequiredMixin, View):
    """图库列表"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'code': 403, 'msg': '请先登录'}, json_dumps_params={'ensure_ascii': False})
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        gallery_queryset = BaykeGallery.objects.all()
        data = serializers.serialize('json', gallery_queryset)
        data = json.loads(data)
        return JsonResponse({'code': 200, 'data': data}, json_dumps_params={'ensure_ascii': False})