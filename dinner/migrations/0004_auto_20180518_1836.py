# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2018-05-18 16:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dinner', '0003_auto_20180517_2041'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='link',
            new_name='forward_link',
        ),
    ]
