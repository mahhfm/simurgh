from django.db import models
from django.contrib.auth.models import User
from datetime import date
from dateutil.relativedelta import relativedelta
from django.utils import timezone
import persian



# an abstract class for all models

class Origin(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Course(Origin):
    level_field = models.ForeignKey("LevelField", on_delete=models.CASCADE, db_constraint=False)
    course_name = models.CharField(max_length=155)
    unite = models.IntegerField()

    def __str__(self):
        return self.course_name + " " + self.level_field.__str__()


class LevelField(Origin):
    L7, L8, L9, L10, L11, L12 = '7', '8', '9', '10', '11', '12'
    LEVEL_CHOICES = (
        (L7, "هفتم"),
        (L8, "هشتم"),
        (L9, "نهم"),
        (L10, "دهم"),
        (L11, "یازدهم"),
        (L12, "دوازدهم"),
    )
    MS, ES, HS = 'ms', 'es', 'hs'
    FIELD_CHOICES = (
        (MS, "ریاضی"),
        (ES, "تجربی"),
        (HS, "انسانی")
    )

    field = models.CharField(max_length=155, choices=FIELD_CHOICES, verbose_name="رشته")
    level = models.CharField(max_length=155, choices=LEVEL_CHOICES, verbose_name="پایه")

    def __str__(self):
        persians = {
            '7': 'هفتم',
            '8': "هشتم",
            '9': "نهم",
            '10': "دهم",
            '11': "یازدهم",
            '12': "دوازدهم",
            'ms': "ریاضی",
            'es': "تجربی",
            'hs': "انسانی",
        }

        return persians[str(self.field)] + " " + persians[str(self.level)]


class ClassRoom(Origin):
    A, B, C = 'a', 'b', 'c'
    BRANCH_CHOICES = (
        (A, "الف"),
        (B, "ب"),
        (C, "ج")
    )
    level_field = models.ForeignKey("LevelField", on_delete=models.CASCADE, db_constraint=False)
    branch = models.CharField(max_length=155, choices=BRANCH_CHOICES, verbose_name="گروه")
    education_year = models.CharField(max_length=10)

    def __str__(self):
        persians = {
            '7': 'هفتم',
            '8': "هشتم",
            '9': "نهم",
            '10': "دهم",
            '11': "یازدهم",
            '12': "دوازدهم",
            'ms': "ریاضی",
            'es': "تجربی",
            'hs': "انسانی",
            'a': "الف",
            'b': "ب",
            'c': "ج",
        }

        return persians[self.level_field.field] + " " + persians[self.level_field.level] + " " + persians[
            self.branch] + " " + self.education_year


class Teacher(Origin):
    BACHELOR, MA, PHD = 'ba', 'ma', 'phd'
    DEGREE_CHOICES = (
        (BACHELOR, "لیسانس"),
        (MA, "فوق لیسانس"),
        (PHD, "دکتری"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_constraint=False)
    hire_date = models.DateField(default=timezone.now)
    education_degree = models.CharField(max_length=155, choices=DEGREE_CHOICES)
    profession = models.ManyToManyField("Course")
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
        return self.user.first_name + " " + self.user.last_name + " " + persian.enToPersianNumb(str(self.tid))


class Student(Origin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_constraint=False)
    classroom = models.ManyToManyField("ClassRoom", through="Register")
    sid = models.BigIntegerField(unique=True)
    courses = models.ManyToManyField("Course", through="StudentCourse")
    profile_image =  models.ImageField(upload_to='profiles/' , default='/profiles/defaults.png')

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + str(persian.enToPersianNumb(self.sid))
    class Meta:
        pass


class Register(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE, db_constraint=False)
    classroom = models.ForeignKey("Classroom", on_delete=models.CASCADE, db_constraint=False)
    active = models.BooleanField()

    def __str__(self):
        return self.student.user.first_name + " " + self.classroom.__str__()


class StudentCourse(Origin):
    student = models.ForeignKey("Student", on_delete=models.CASCADE, db_constraint=False)
    courses = models.ForeignKey("Course", on_delete=models.CASCADE, db_constraint=False)
    final_grade = models.FloatField()
    mid_grade = models.FloatField()

    def __str__(self):
        return self.student.user.first_name + " " + self.courses.course_name + " " + str(
            persian.enToPersianNumb(self.final_grade))


class TCC(Origin):
    teacher = models.ForeignKey("Teacher", on_delete=models.CASCADE, db_constraint=False)
    course = models.ForeignKey("Course", on_delete=models.CASCADE, db_constraint=False)
    classroom = models.ForeignKey("Classroom", on_delete=models.CASCADE, db_constraint=False)
    class_time = models.CharField(max_length=155)

    def __str__(self):
        return self.teacher.user.first_name + " " + self.course.__str__() + " " + self.classroom.__str__()


class Parent(Origin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_constraint=False)
    related_student=models.ForeignKey("Student", on_delete=models.CASCADE, db_constraint=False)


class StudentAttendance(Origin):
    register = models.ForeignKey("Register", on_delete=models.CASCADE, db_constraint=False)
    present = models.BooleanField()
    present_date = models.DateField(default=timezone.now)
    def __str__(self):
        return str(self.register.student.user) + " " + str(self.register.classroom)
    
class TeacherAttendance(Origin):
    teacher = models.ForeignKey("Teacher", on_delete=models.CASCADE, db_constraint=False)
    present = models.BooleanField()
    present_date = models.DateField(default=timezone.now)

