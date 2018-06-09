# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FEA2D', '0002_auto_20180419_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feainput',
            name='email',
            field=models.EmailField(max_length=75),
        ),
    ]
