from rest_framework import serializers


class UploadImageSerializer(serializers.Serializer):
    file = serializers.ImageField()