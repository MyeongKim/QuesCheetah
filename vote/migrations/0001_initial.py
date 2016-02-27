# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(max_length=50)),
                ('answer_num', models.IntegerField(null=True)),
                ('created_dt', models.DateTimeField(auto_now_add=True)),
                ('updated_dt', models.DateTimeField(auto_now=True)),
                ('is_removed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='MultiQuestion',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=100, unique=True)),
                ('created_dt', models.DateTimeField(auto_now_add=True)),
                ('updated_dt', models.DateTimeField(auto_now=True)),
                ('is_removed', models.BooleanField(default=False)),
                ('api_key', models.ForeignKey(related_name='multiquestions', to='main.ApiKey')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=60, choices=[('SURV', 'Survey'), ('VOTE', 'Vote')], default='VOTE')),
                ('question_title', models.CharField(max_length=50)),
                ('question_text', models.CharField(max_length=100)),
                ('question_num', models.CharField(max_length=10, null=True)),
                ('is_closed', models.BooleanField(default=False)),
                ('start_dt', models.DateTimeField()),
                ('end_dt', models.DateTimeField()),
                ('is_editable', models.BooleanField(default=True)),
                ('is_private', models.BooleanField(default=False)),
                ('is_removed', models.BooleanField(default=False)),
                ('created_dt', models.DateTimeField(auto_now_add=True)),
                ('updated_dt', models.DateTimeField(auto_now=True)),
                ('api_key', models.ForeignKey(related_name='questions', to='main.ApiKey')),
                ('multi_question', models.ForeignKey(related_name='question_elements', to='vote.MultiQuestion', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('unique_user', models.CharField(max_length=100, unique=True)),
                ('created_dt', models.DateTimeField(auto_now_add=True)),
                ('updated_dt', models.DateTimeField(auto_now=True)),
                ('is_removed', models.BooleanField(default=False)),
                ('answer', models.ForeignKey(related_name='answer', to='vote.Answer')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(related_name='answers', to='vote.Question'),
        ),
    ]
