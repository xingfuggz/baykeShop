# Generated by Django 4.2.17 on 2024-12-10 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_baykeshoporders_is_verify'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baykeshopgoodssku',
            name='line_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text='商品价格划线价，不参与价位计算筛选, 仅供前端显示使用', max_digits=10, verbose_name='划线价'),
        ),
        migrations.AlterField(
            model_name='baykeshopgoodssku',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='价格'),
        ),
    ]
