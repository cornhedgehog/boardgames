# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-14 00:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0003_auto_20171012_0046'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostStarred',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='body_preview',
            field=models.CharField(default='body preview', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='blog_posts', to='blog.Category'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='subtitle',
            field=models.CharField(default='subtitle', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='poststarred',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts_starred', to='blog.Post'),
        ),
        migrations.AddField(
            model_name='poststarred',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts_starred', to=settings.AUTH_USER_MODEL),
        ),
    ]