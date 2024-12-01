# Generated by Django 5.1.2 on 2024-11-25 09:07

import baykeshop.apps.core.validators._validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, default='', upload_to='avatar/%Y/%m', validators=[baykeshop.apps.core.validators._validators.validate_image_size], verbose_name='头像'),
        ),
    ]
