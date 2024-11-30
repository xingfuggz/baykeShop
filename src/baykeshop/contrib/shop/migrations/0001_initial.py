# Generated by Django 4.2.16 on 2024-11-29 08:12

from django.conf import settings
import django.contrib.sites.managers
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaykeShopBrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, editable=False, verbose_name='是否删除')),
                ('name', models.CharField(max_length=50, verbose_name='品牌名称')),
                ('image', models.ImageField(blank=True, null=True, upload_to='brand', verbose_name='品牌图片')),
                ('order', models.IntegerField(default=0, verbose_name='排序')),
                ('description', models.TextField(blank=True, null=True, verbose_name='品牌介绍')),
                ('site', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='sites.site', verbose_name='站点')),
            ],
            options={
                'verbose_name': '商品品牌',
                'verbose_name_plural': '商品品牌',
                'ordering': ['order'],
            },
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('current_site', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.CreateModel(
            name='BaykeShopCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, editable=False, verbose_name='是否删除')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否显示')),
                ('order', models.IntegerField(default=0, verbose_name='排序')),
                ('icon', models.CharField(blank=True, default='', max_length=50, verbose_name='图标')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.baykeshopcategory', verbose_name='父级')),
                ('site', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='sites.site', verbose_name='站点')),
            ],
            options={
                'verbose_name': '商品分类',
                'verbose_name_plural': '商品分类',
                'ordering': ['order'],
            },
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('current_site', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.CreateModel(
            name='BaykeShopGoods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, editable=False, verbose_name='是否删除')),
                ('name', models.CharField(max_length=50, verbose_name='商品名称')),
                ('keywords', models.CharField(blank=True, max_length=255, null=True, verbose_name='商品关键字')),
                ('description', models.TextField(blank=True, null=True, verbose_name='商品描述')),
                ('detail', models.TextField(blank=True, null=True, verbose_name='商品详情')),
                ('spec_type', models.PositiveSmallIntegerField(choices=[(1, '单规格'), (2, '多规格')], default=1, verbose_name='商品规格类型')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, '上架'), (2, '下架')], default=1, verbose_name='商品状态')),
                ('goods_type', models.PositiveSmallIntegerField(choices=[(1, '普通商品'), (2, '虚拟商品')], default=1, verbose_name='商品类型')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.baykeshopbrand', verbose_name='商品品牌')),
                ('category', models.ManyToManyField(blank=True, to='shop.baykeshopcategory', verbose_name='商品分类')),
                ('site', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='sites.site', verbose_name='站点')),
            ],
            options={
                'verbose_name': '商品',
                'verbose_name_plural': '商品',
                'ordering': ['-created_time'],
            },
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('current_site', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.CreateModel(
            name='BaykeShopGoodsSKU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, editable=False, verbose_name='是否删除')),
                ('specs', models.JSONField(blank=True, default=list, help_text='规格数据', verbose_name='规格')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='价格')),
                ('sku_sn', models.CharField(blank=True, default='', max_length=50, verbose_name='商品编码')),
                ('line_price', models.DecimalField(blank=True, decimal_places=2, default='', help_text='商品价格划线价，不参与价位计算筛选, 仅供前端显示使用', max_digits=10, verbose_name='划线价')),
                ('stock', models.PositiveSmallIntegerField(default=0, verbose_name='库存')),
                ('sales', models.PositiveSmallIntegerField(default=0, verbose_name='销量')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.baykeshopgoods', verbose_name='商品')),
                ('site', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='sites.site', verbose_name='站点')),
            ],
            options={
                'verbose_name': '商品SKU',
                'verbose_name_plural': '商品SKU',
                'ordering': ['-created_time'],
            },
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('current_site', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.CreateModel(
            name='BaykeShopOrders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, editable=False, verbose_name='是否删除')),
                ('order_sn', models.CharField(max_length=50, verbose_name='订单号')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='总价')),
                ('status', models.IntegerField(choices=[(0, '未支付'), (1, '待发货'), (2, '待收货'), (3, '已完成'), (4, '已取消'), (5, '已过期'), (6, '待核销'), (7, '已核销')], default=0, verbose_name='订单状态')),
                ('pay_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='实际支付金额')),
                ('receiver', models.CharField(blank=True, default='', max_length=50, verbose_name='收货人')),
                ('phone', models.CharField(blank=True, default='', max_length=11, verbose_name='手机号码')),
                ('address', models.CharField(blank=True, default='', max_length=255, verbose_name='收货地址')),
                ('pay_type', models.IntegerField(choices=[(1, '支付宝'), (2, '微信支付'), (3, '货到付款')], default=1, verbose_name='支付方式')),
                ('pay_sn', models.CharField(blank=True, default='', max_length=32, verbose_name='支付流水号')),
                ('pay_time', models.DateTimeField(blank=True, null=True, verbose_name='支付时间')),
                ('is_verify', models.BooleanField(default=False, verbose_name='是否核销订单')),
                ('verify_time', models.DateTimeField(blank=True, null=True, verbose_name='核销时间')),
                ('is_comment', models.BooleanField(default=False, verbose_name='是否评价')),
                ('site', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='sites.site', verbose_name='站点')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '订单',
                'verbose_name_plural': '订单',
                'ordering': ['-created_time'],
                'abstract': False,
            },
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('current_site', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.CreateModel(
            name='BaykeShopSpec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, editable=False, verbose_name='是否删除')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否显示')),
                ('order', models.IntegerField(default=0, verbose_name='排序')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.baykeshopspec', verbose_name='父级')),
                ('site', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='sites.site', verbose_name='站点')),
            ],
            options={
                'verbose_name': '规格模版',
                'verbose_name_plural': '规格模版',
                'ordering': ['-created_time'],
            },
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('current_site', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.CreateModel(
            name='BaykeShopOrdersGoods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, editable=False, verbose_name='是否删除')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='价格')),
                ('quantity', models.IntegerField(default=1, verbose_name='数量')),
                ('specs', models.JSONField(blank=True, default=list, help_text='规格数据', verbose_name='规格')),
                ('sku_sn', models.CharField(blank=True, default='', max_length=50, verbose_name='商品编码')),
                ('name', models.CharField(blank=True, default='', max_length=50, verbose_name='商品名称')),
                ('detail', models.TextField(blank=True, null=True, verbose_name='商品详情')),
                ('image', models.ImageField(blank=True, null=True, upload_to='goods', verbose_name='商品主图')),
                ('orders', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.baykeshoporders', verbose_name='订单')),
                ('site', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='sites.site', verbose_name='站点')),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.baykeshopgoodssku', verbose_name='商品')),
            ],
            options={
                'verbose_name': '订单商品',
                'verbose_name_plural': '订单商品',
                'ordering': ['-created_time'],
            },
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('current_site', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.CreateModel(
            name='BaykeShopGoodsImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, editable=False, verbose_name='是否删除')),
                ('image', models.ImageField(upload_to='goods/images', verbose_name='商品图片')),
                ('order', models.IntegerField(default=0, verbose_name='排序')),
                ('is_main', models.BooleanField(default=False, verbose_name='是否主图')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.baykeshopgoods', verbose_name='商品')),
                ('site', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='sites.site', verbose_name='站点')),
            ],
            options={
                'verbose_name': '商品图片',
                'verbose_name_plural': '商品图片',
                'ordering': ['order'],
            },
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('current_site', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.CreateModel(
            name='BaykeShopCarts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, editable=False, verbose_name='是否删除')),
                ('quantity', models.IntegerField(default=1, verbose_name='数量')),
                ('site', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='sites.site', verbose_name='站点')),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.baykeshopgoodssku', verbose_name='商品')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '购物车',
                'verbose_name_plural': '购物车',
                'ordering': ['-created_time'],
            },
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('current_site', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.AddConstraint(
            model_name='baykeshopordersgoods',
            constraint=models.UniqueConstraint(fields=('sku', 'orders'), name='sku_orders_unique'),
        ),
        migrations.AddConstraint(
            model_name='baykeshoporders',
            constraint=models.UniqueConstraint(fields=('user', 'order_sn'), name='unique_order_sn'),
        ),
        migrations.AddConstraint(
            model_name='baykeshopgoodsimages',
            constraint=models.UniqueConstraint(fields=('goods', 'is_main'), name='unique_goods_image'),
        ),
        migrations.AddConstraint(
            model_name='baykeshopcarts',
            constraint=models.UniqueConstraint(fields=('user', 'sku'), name='unique_carts'),
        ),
    ]
