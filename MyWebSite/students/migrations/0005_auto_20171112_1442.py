# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_auto_20171112_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluationquestion',
            name='visualizationId',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='evaluationanswer',
            name='answer',
            field=models.SmallIntegerField(choices=[(1, '\u975e\u5e38\u6c92\u6709\u5e6b\u52a9'), (2, '\u6c92\u6709\u5e6b\u52a9'), (3, '\u4e0d\u592a\u6709\u5e6b\u52a9'), (4, '\u6709\u5e6b\u52a9'), (5, '\u5f88\u6709\u5e6b\u52a9'), (6, '\u975e\u5e38\u6709\u5e6b\u52a9')]),
        ),
    ]
