#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件    :views.py
@说明    :上传图片视图
@时间    :2024/12/07 17:41:53
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
"""
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from .serializers import UploadImageSerializer


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """关闭csrf验证"""

    def enforce_csrf(self, request):
        return


class UploadImageView(GenericAPIView):
    serializer_class = UploadImageSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """上传图片"""
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        image = serializer.validated_data["file"]
        # 上传到指定目录
        storeage = FileSystemStorage(
            location=settings.MEDIA_ROOT / "uploads",
            base_url=settings.MEDIA_URL + "uploads/",
        )
        file_name = storeage.save(image.name, image)
        url = storeage.url(file_name)
        return Response({"location": url})
