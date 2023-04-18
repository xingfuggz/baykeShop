from django.test import TestCase
from . import models

class BaykeArticleCategoryCase(TestCase):
    def setUp(self):
        models.BaykeArticleCategory.objects.create(name="分类一")
        models.BaykeArticleCategory.objects.create(name="分类二")

    def test_cate_can_create(self):
        cates = models.BaykeArticleCategory.objects.all()
        self.assertEqual(cates.count(), 2)
        