# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('second_lection_exist', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Mess',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('speech_number', models.PositiveIntegerField(default=0)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='mess',
            name='believers_pray',
            field=models.ForeignKey(related_name='believers_pray_users', to='lister.Reader'),
        ),
        migrations.AddField(
            model_name='mess',
            name='day',
            field=models.ForeignKey(to='lister.Day'),
        ),
        migrations.AddField(
            model_name='mess',
            name='first_lection',
            field=models.ForeignKey(related_name='first_lection_users', to='lister.Reader'),
        ),
        migrations.AddField(
            model_name='mess',
            name='psalm',
            field=models.ForeignKey(related_name='psalm_users', to='lister.Reader'),
        ),
        migrations.AddField(
            model_name='mess',
            name='second_lection',
            field=models.ForeignKey(related_name='second_lection_users', to='lister.Reader'),
        ),
    ]
