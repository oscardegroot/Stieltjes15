# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-11-22 16:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picnic', '0005_auto_20171122_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.FileField(default='images/anonymous.jpg', upload_to=''),
        ),
    ]
