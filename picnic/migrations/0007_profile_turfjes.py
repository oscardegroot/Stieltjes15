# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-11-22 17:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picnic', '0006_auto_20171122_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='turfjes',
            field=models.IntegerField(default=0),
        ),
    ]
