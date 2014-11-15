# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_auto_20141017_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='student',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
