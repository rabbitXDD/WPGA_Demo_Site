# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_auto_20160829_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='MondayClass',
            field=models.BooleanField(default=True),
        ),
    ]
