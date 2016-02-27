# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, blank=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('email', models.EmailField(max_length=250, unique=True)),
                ('username', models.CharField(max_length=250, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.NullBooleanField(default=True)),
                ('is_staff', models.NullBooleanField(default=False)),
                ('groups', models.ManyToManyField(verbose_name='groups', related_name='user_set', to='auth.Group', related_query_name='user', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.')),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', related_name='user_set', to='auth.Permission', related_query_name='user', blank=True, help_text='Specific permissions for this user.')),
            ],
            options={
                'swappable': 'AUTH_USER_MODEL',
            },
        ),
        migrations.CreateModel(
            name='ApiKey',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=40)),
                ('secret_key', models.CharField(max_length=100, null=True)),
                ('created_dt', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(related_name='api_keys', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=100)),
                ('created_dt', models.DateTimeField(auto_now_add=True)),
                ('updated_dt', models.DateTimeField(auto_now=True)),
                ('is_removed', models.BooleanField(default=False)),
                ('api_key', models.ForeignKey(related_name='domains', to='main.ApiKey')),
            ],
        ),
    ]
