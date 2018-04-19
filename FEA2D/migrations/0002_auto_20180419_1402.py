# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FEA2D', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feainput',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
