# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2018-09-22 14:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dinner', '0006_dinnerdate_boodschap_feuten'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dinnerdate',
            unique_together=set([('date',)]),
        ),
    ]
