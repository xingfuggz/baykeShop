from rest_framework import serializers

from baykeshop.module.article.models import BaykeArticle, BaykeArticleCategory, BaykeArticleTag


class BaykeArticleTagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BaykeArticleTag
        fields = "__all__"


class BaykeArticleSerializer(serializers.ModelSerializer):
    
    tags = BaykeArticleTagSerializer(many=True)
    category = serializers.StringRelatedField(many=False)
    
    class Meta:
        model = BaykeArticle
        fields = "__all__"


class BaykeArticleCategorySerializer(serializers.ModelSerializer):
    
    baykearticle_set = BaykeArticleSerializer(many=True)
    
    class Meta:
        model = BaykeArticleCategory
        fields = "__all__"
        

