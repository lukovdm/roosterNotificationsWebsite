# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0004_user_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='teacher',
            field=models.TextField(default=b'aaa', max_length=3),
            preserve_default=True,
        ),
    ]
