from django.db import models
from django.contrib.auth.models import User
from datetime import date
from dateutil.relativedelta import relativedelta
import persian


class Course(models.Model):
    course_name = models.CharField(max_length=155)

    def __str__(self):
        return self.course_name


class ClassRoom(models.Model):
    MS, ES, HS = 'ms', 'es', 'hs'
    FIELD_CHOICES = (
        (MS, "ریاضی"),
        (ES, "تجربی"),
        (HS, "انسانی")
    )

    A, B, C = 'a', 'b', 'c'
    GROUP_CHOICES = (
        (A, "الف"),
        (B, "ب"),
        (C, "ج")
    )

    L7, L8, L9, L10, L11, L12 = '7', '8', '9', '10', '11', '12'
    LEVEL_CHOICES = (
        (L7, "هفتم"),
        (L8, "هشتم"),
        (L9, "نهم"),
        (L10, "دهم"),
        (L11, "یازدهم"),
        (L12, "دوازدهم"),
    )

    level = models.CharField(max_length=155, choices=LEVEL_CHOICES, verbose_name="پایه")
    group = models.CharField(max_length=155, choices=GROUP_CHOICES, verbose_name="گروه")
    field = models.CharField(max_length=155, choices=FIELD_CHOICES, verbose_name="رشته")

    def get_math_student(self):
        self.objects.filter(field=self.MS)

    def __str__(self):
        persians = {
            '7': 'هفتم',
            '8': "هشتم",
            '9': "نهم",
            '10': "دهم",
            '11': "یازدهم",
            '12': "دوازدهم",
            'a': "الف",
            'b': "ب",
            'c': "ج",
            'ms': "ریاضی",
            'es': "تجربی",
            'hs': "انسانی",
        }

        return "کلاس " + persians[self.field] + " پایه " + persians[self.level] + " " + persians[self.group]


class Teacher(models.Model):
    BACHELOR, MA, PHD = 'ba', 'ma', 'phd'
    DEGREE_CHOICES = (
        (BACHELOR, "لیسانس"),
        (MA, "فوق لیسانس"),
        (PHD, "دکتری"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hire_date = models.DateField(default=date.today())
    education_degree = models.CharField(max_length=155, choices=DEGREE_CHOICES)
    profession = models.ForeignKey("Course", on_delete=models.CASCADE)
    classroom = models.ManyToManyField("ClassRoom")
    tid = models.BigIntegerField(unique=True)

    @property
    def experience(self):
        delta = relativedelta(date.today(), self.hire_date)
        year = persian.enToPersianNumb(str(delta.years))
        month = persian.enToPersianNumb(str(delta.months))
        days = persian.enToPersianNumb(str(delta.days))
        return "{} سال و {} ماه و {} روز".format(year, month, days)

    experiences = experience

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey("ClassRoom", on_delete=models.CASCADE)
    sid = models.BigIntegerField(unique=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + str(self.sid)
