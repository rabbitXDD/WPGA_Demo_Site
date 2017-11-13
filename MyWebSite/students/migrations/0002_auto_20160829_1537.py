# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='student',
            field=models.ForeignKey(related_name='grade', to='students.Student'),
        ),
    ]
