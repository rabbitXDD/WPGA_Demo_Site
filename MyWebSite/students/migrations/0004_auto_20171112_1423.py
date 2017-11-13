# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_user_mondayclass'),
    ]

    operations = [
        migrations.CreateModel(
            name='EvaluationAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.SmallIntegerField(choices=[(0, 'Good'), (0, 'Good'), (1, 'Bad'), (2, 'Dunno'), (3, 'Bravo')])),
            ],
        ),
        migrations.CreateModel(
            name='EvaluationQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='EvaluationScheme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='evaluationquestion',
            name='evaluation',
            field=models.ForeignKey(to='students.EvaluationScheme'),
        ),
        migrations.AddField(
            model_name='evaluationanswer',
            name='question',
            field=models.ForeignKey(to='students.EvaluationQuestion'),
        ),
        migrations.AddField(
            model_name='evaluationanswer',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
