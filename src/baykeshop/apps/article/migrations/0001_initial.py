# Generated by Django 5.1.2 on 2024-11-25 08:02

import baykeshop.apps.core.utils.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaykeArticleTags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_show', models.BooleanField(default=True, editable=False, help_text='不显示在页面上', verbose_name='是否显示')),
                ('name', models.CharField(max_length=50, verbose_name='标签名称')),
            ],
            options={
                'verbose_name': '文章标签',
                'verbose_name_plural': '文章标签',
                'ordering': ['-create_time'],
            },
        ),
        migrations.CreateModel(
            name='BaykeArticleCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=50, verbose_name='分类名称')),
                ('description', models.TextField(blank=True, default='', verbose_name='描述')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否显示')),
                ('sort', models.IntegerField(default=0, verbose_name='排序')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='article.baykearticlecategory', verbose_name='父级分类')),
            ],
            options={
                'verbose_name': '文章分类',
                'verbose_name_plural': '文章分类',
                'ordering': ['sort'],
            },
        ),
        migrations.CreateModel(
            name='BaykeArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('desc', models.CharField(blank=True, default='', help_text='文章描述，用于SEO优化', max_length=150, verbose_name='描述')),
                ('content', baykeshop.apps.core.utils.fields.RichTextField(verbose_name='内容')),
                ('image', models.ImageField(blank=True, null=True, upload_to='article/%Y/%m/%d', verbose_name='图片')),
                ('is_top', models.BooleanField(default=False, verbose_name='置顶')),
                ('is_recommend', models.BooleanField(default=False, verbose_name='推荐')),
                ('is_original', models.BooleanField(default=False, verbose_name='原创')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否显示')),
                ('sort', models.IntegerField(default=0, verbose_name='排序')),
                ('author', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.baykearticlecategory', verbose_name='分类')),
                ('tags', models.ManyToManyField(blank=True, to='article.baykearticletags', verbose_name='标签')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
                'ordering': ['sort'],
            },
        ),
    ]
