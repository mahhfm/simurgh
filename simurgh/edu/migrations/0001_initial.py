# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-04-12 06:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('7', 'هفتم'), ('8', 'هشتم'), ('9', 'نهم'), ('10', 'دهم'), ('11', 'یازدهم'), ('12', 'دوازدهم')], max_length=155)),
                ('group', models.CharField(choices=[('a', 'الف'), ('b', 'ب'), ('c', 'ج')], max_length=155, verbose_name='گروه')),
                ('field', models.CharField(choices=[('ms', 'ریاضی'), ('es', 'تجربی'), ('hs', 'انسانی')], max_length=155)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=155)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sid', models.BigIntegerField(unique=True)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edu.ClassRoom')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hire_date', models.DateField(auto_now_add=True)),
                ('education_degree', models.CharField(choices=[('ba', 'لیسانس'), ('ma', 'فوق لیسانس'), ('phd', 'دکتری')], max_length=155)),
                ('tid', models.BigIntegerField(max_length=155, unique=True)),
                ('classroome', models.ManyToManyField(to='edu.ClassRoom')),
                ('profession', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edu.Course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
