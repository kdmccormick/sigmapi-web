# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-10-21 20:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PartyListV2', '0009_auto_20181021_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='partyguest',
            name='_cached_json',
            field=models.TextField(null=True),
        ),
    ]