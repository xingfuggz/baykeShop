# Generated by Django 4.2.17 on 2024-12-07 14:11

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
            name='BaykeShopUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, editable=False, verbose_name='是否删除')),
                ('nickname', models.CharField(blank=True, max_length=50, null=True, verbose_name='昵称')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatar', verbose_name='头像')),
                ('gender', models.CharField(choices=[('male', '男'), ('female', '女'), ('unknown', '未知')], default='male', max_length=10, verbose_name='性别')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='生日')),
                ('mobile', models.CharField(blank=True, max_length=11, null=True, unique=True, verbose_name='手机号码')),
                ('qq', models.CharField(blank=True, max_length=20, null=True, verbose_name='QQ')),
                ('wechat', models.CharField(blank=True, max_length=50, null=True, verbose_name='微信')),
                ('description', models.TextField(blank=True, null=True, verbose_name='简介')),
                ('site', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='sites.site', verbose_name='站点')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
                'ordering': ['-created_time'],
                'abstract': False,
            },
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('current_site', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.CreateModel(
            name='BaykeShopUserAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, editable=False, verbose_name='是否删除')),
                ('name', models.CharField(max_length=50, verbose_name='收货人')),
                ('province', models.CharField(max_length=50, verbose_name='省')),
                ('city', models.CharField(max_length=50, verbose_name='市')),
                ('district', models.CharField(max_length=50, verbose_name='区')),
                ('address', models.CharField(max_length=255, verbose_name='详细地址')),
                ('phone', models.CharField(max_length=50, verbose_name='手机')),
                ('is_default', models.BooleanField(default=False, verbose_name='是否默认')),
                ('site', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='sites.site', verbose_name='站点')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户地址',
                'verbose_name_plural': '用户地址',
                'ordering': ['-created_time'],
                'indexes': [models.Index(fields=['user', 'is_default'], name='user_is_default_idx')],
            },
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('current_site', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
    ]
