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
            name='BaykeShopBrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_show', models.BooleanField(default=True, editable=False, help_text='不显示在页面上', verbose_name='是否显示')),
                ('name', models.CharField(max_length=50, verbose_name='品牌名称')),
                ('description', models.TextField(blank=True, default='', verbose_name='描述')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='brand/%Y/%m/%d', verbose_name='品牌logo')),
                ('sort', models.IntegerField(default=0, verbose_name='排序')),
                ('website', models.URLField(blank=True, default='', verbose_name='官网')),
            ],
            options={
                'verbose_name': '品牌',
                'verbose_name_plural': '品牌',
                'ordering': ['sort', '-create_time'],
            },
        ),
        migrations.CreateModel(
            name='BaykeShopGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('image', models.ImageField(upload_to='gallery/%Y/%m/%d', verbose_name='图片')),
                ('target', models.CharField(blank=True, max_length=128, verbose_name='跳转地址')),
                ('desc', models.CharField(blank=True, default='', max_length=128, verbose_name='描述')),
                ('sort', models.IntegerField(default=0, verbose_name='排序')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否显示')),
            ],
            options={
                'verbose_name': '商城轮播图',
                'verbose_name_plural': '商城轮播图',
                'ordering': ['sort'],
            },
        ),
        migrations.CreateModel(
            name='BaykeShopSpec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_show', models.BooleanField(default=True, editable=False, help_text='不显示在页面上', verbose_name='是否显示')),
                ('name', models.CharField(max_length=50, verbose_name='规格类名')),
            ],
            options={
                'verbose_name': '商品规格',
                'verbose_name_plural': '商品规格',
                'ordering': ['-create_time'],
            },
        ),
        migrations.CreateModel(
            name='BaykeShopCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_show', models.BooleanField(default=True, editable=False, help_text='不显示在页面上', verbose_name='是否显示')),
                ('name', models.CharField(max_length=50, verbose_name='分类名称')),
                ('icon', models.CharField(blank=True, default='', max_length=50, verbose_name='图标')),
                ('is_floor', models.BooleanField(default=False, verbose_name='是否楼层')),
                ('is_nav', models.BooleanField(default=False, verbose_name='是否导航')),
                ('sort', models.IntegerField(default=0, verbose_name='排序')),
                ('pid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.baykeshopcategory', verbose_name='父级分类')),
            ],
            options={
                'verbose_name': '商品分类',
                'verbose_name_plural': '商品分类',
                'ordering': ['sort', '-create_time'],
            },
        ),
        migrations.CreateModel(
            name='BaykeShopSpecValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_show', models.BooleanField(default=True, editable=False, help_text='不显示在页面上', verbose_name='是否显示')),
                ('value', models.CharField(max_length=50, verbose_name='规格值')),
                ('spec', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.baykeshopspec', verbose_name='规格')),
            ],
            options={
                'verbose_name': '规格值',
                'verbose_name_plural': '规格值',
                'ordering': ['-create_time'],
            },
        ),
        migrations.CreateModel(
            name='BaykeShopSpecValueCombination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_show', models.BooleanField(default=True, editable=False, help_text='不显示在页面上', verbose_name='是否显示')),
                ('specs', models.ManyToManyField(to='shop.baykeshopspecvalue', verbose_name='规格')),
            ],
            options={
                'verbose_name': '规格组合',
                'verbose_name_plural': '规格组合',
                'ordering': ['-create_time'],
            },
        ),
        migrations.CreateModel(
            name='BaykeShopSPU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_show', models.BooleanField(default=True, editable=False, help_text='不显示在页面上', verbose_name='是否显示')),
                ('name', models.CharField(max_length=100, verbose_name='商品名称')),
                ('description', models.TextField(blank=True, default='', verbose_name='描述')),
                ('keywords', models.CharField(blank=True, default='', max_length=100, verbose_name='关键字')),
                ('content', baykeshop.apps.core.utils.fields.RichTextField(verbose_name='商品详情')),
                ('image', models.ImageField(blank=True, null=True, upload_to='goods/%Y/%m/%d', verbose_name='图片')),
                ('is_boutique', models.BooleanField(default=False, verbose_name='精品')),
                ('is_new', models.BooleanField(default=False, verbose_name='新品')),
                ('is_recommend', models.BooleanField(default=False, verbose_name='推荐')),
                ('is_on_sale', models.BooleanField(default=True, verbose_name='是否上架')),
                ('sort', models.IntegerField(default=0, verbose_name='排序')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.baykeshopbrand', verbose_name='品牌')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.baykeshopcategory', verbose_name='分类')),
            ],
            options={
                'verbose_name': '商品',
                'verbose_name_plural': '商品',
                'ordering': ['-create_time'],
            },
        ),
        migrations.CreateModel(
            name='BaykeShopSKU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_show', models.BooleanField(default=True, editable=False, help_text='不显示在页面上', verbose_name='是否显示')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='价格')),
                ('stock', models.PositiveBigIntegerField(default=0, verbose_name='库存')),
                ('num', models.PositiveBigIntegerField(default=0, editable=False, verbose_name='销量')),
                ('sort', models.IntegerField(default=0, verbose_name='排序')),
                ('unit', models.CharField(blank=True, default='件', max_length=50, verbose_name='单位')),
                ('combination', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.baykeshopspecvaluecombination', verbose_name='规格组合')),
                ('spu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.baykeshopspu', verbose_name='SPU')),
            ],
            options={
                'verbose_name': '商品SKU',
                'verbose_name_plural': '商品SKU',
                'ordering': ['sort', '-create_time'],
            },
        ),
        migrations.CreateModel(
            name='BaykeShopSPUGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_show', models.BooleanField(default=True, editable=False, help_text='不显示在页面上', verbose_name='是否显示')),
                ('image', models.ImageField(blank=True, null=True, upload_to='goods/%Y/%m/%d', verbose_name='图片')),
                ('sort', models.IntegerField(default=0, verbose_name='排序')),
                ('spu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.baykeshopspu', verbose_name='商品')),
            ],
            options={
                'verbose_name': '商品轮播图',
                'verbose_name_plural': '商品轮播图',
                'ordering': ['sort', '-create_time'],
            },
        ),
        migrations.CreateModel(
            name='BaykeShopCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_show', models.BooleanField(default=True, editable=False, help_text='不显示在页面上', verbose_name='是否显示')),
                ('num', models.PositiveIntegerField(default=1, verbose_name='数量')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.baykeshopsku', verbose_name='商品')),
            ],
            options={
                'verbose_name': '购物车',
                'verbose_name_plural': '购物车',
                'ordering': ['-create_time'],
                'constraints': [models.UniqueConstraint(fields=('user', 'sku'), name='unique_cart')],
            },
        ),
        migrations.AddConstraint(
            model_name='baykeshopspecvalue',
            constraint=models.UniqueConstraint(fields=('spec', 'value'), name='unique_spec_value'),
        ),
        migrations.AddConstraint(
            model_name='baykeshopsku',
            constraint=models.UniqueConstraint(fields=('spu', 'combination'), name='unique_spu_combination'),
        ),
    ]
