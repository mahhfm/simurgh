# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-16 04:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


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
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('branch', models.CharField(choices=[('a', 'الف'), ('b', 'ب'), ('c', 'ج')], max_length=155, verbose_name='گروه')),
                ('education_year', models.CharField(max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('course_name', models.CharField(max_length=155)),
                ('unite', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LevelField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('field', models.CharField(choices=[('ms', 'ریاضی'), ('es', 'تجربی'), ('hs', 'انسانی')], max_length=155, verbose_name='رشته')),
                ('level', models.CharField(choices=[('7', 'هفتم'), ('8', 'هشتم'), ('9', 'نهم'), ('10', 'دهم'), ('11', 'یازدهم'), ('12', 'دوازدهم')], max_length=155, verbose_name='پایه')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField()),
                ('classroom', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='edu.ClassRoom')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('sid', models.BigIntegerField(unique=True)),
                ('profile_image', models.FileField(upload_to='')),
                ('classroom', models.ManyToManyField(through='edu.Register', to='edu.ClassRoom')),
            ],
        ),
        migrations.CreateModel(
            name='StudentCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('final_grade', models.FloatField()),
                ('mid_grade', models.FloatField()),
                ('courses', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='edu.Course')),
                ('student', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='edu.Student')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TCC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('class_time', models.CharField(max_length=155)),
                ('classroom', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='edu.ClassRoom')),
                ('course', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='edu.Course')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('hire_date', models.DateField(default=django.utils.timezone.now)),
                ('education_degree', models.CharField(choices=[('ba', 'لیسانس'), ('ma', 'فوق لیسانس'), ('phd', 'دکتری')], max_length=155)),
                ('tid', models.BigIntegerField(unique=True)),
                ('classroom', models.ManyToManyField(to='edu.ClassRoom')),
                ('profession', models.ManyToManyField(to='edu.Course')),
                ('user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='tcc',
            name='teacher',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='edu.Teacher'),
        ),
        migrations.AddField(
            model_name='student',
            name='courses',
            field=models.ManyToManyField(through='edu.StudentCourse', to='edu.Course'),
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='register',
            name='student',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='edu.Student'),
        ),
        migrations.AddField(
            model_name='course',
            name='level_field',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='edu.LevelField'),
        ),
        migrations.AddField(
            model_name='classroom',
            name='level_field',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='edu.LevelField'),
        ),
    ]