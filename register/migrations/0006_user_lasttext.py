# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0005_user_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='lastText',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
    ]
