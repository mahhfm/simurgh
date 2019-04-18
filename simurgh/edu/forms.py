from django import forms
from .models import Course, ClassRoom


class NewStudent(forms.Form):
    LEVEL_CHOICES = [
        ("7", "هفتم"),
        ("8", "هشتم"),
        ("9", "نهم"),
        ("10", "دهم"),
        ("11", "یازدهم"),
        ("12", "دوازدهم"),
    ]

    GROUP_CHOICES = (
        ("a", "الف"),
        ("b", "ب"),
        ("c", "ج")
    )

    FIELD_CHOICES = (
        ("ms", "ریاضی"),
        ("es", "تجربی"),
        ("hs", "انسانی")
    )

    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-group'}), label="نام")
    family = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-group'}),
                             label="نام خانوادگی")
    email = forms.EmailField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-group'}), label="ایمیل ")
    level = forms.ChoiceField(choices=LEVEL_CHOICES, widget=forms.Select(attrs={'class': 'form-group'}),
                              label="پایه")
    group = forms.ChoiceField(choices=GROUP_CHOICES, widget=forms.Select(attrs={'class': 'form-group'}), label=" گروه")
    field = forms.ChoiceField(choices=FIELD_CHOICES, widget=forms.Select(attrs={'class': 'form-group'}), label="رشته ")
    username = forms.CharField(max_length=255, label="نام کاربری")
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(), label="رمز عبور")


class NewTeacher(forms.Form):
    CLASS_CHOICES = [[cls.id, cls.__str__()] for cls in ClassRoom.objects.all()]
    COURSE_CHOICES = [[course.id, course.course_name] for course in Course.objects.all()]

    BACHELOR, MA, PHD = 'ba', 'ma', 'phd'
    DEGREE_CHOICES = (
        (BACHELOR, "لیسانس"),
        (MA, "فوق لیسانس"),
        (PHD, "دکتری"),
    )

    name = forms.CharField(max_length=255, label="نام")
    family = forms.CharField(max_length=255, label="نام خانوادگی")
    email = forms.EmailField(max_length=255, label="ایمیل ")
    education_degree = forms.ChoiceField(
        widget=forms.Select,
        choices=DEGREE_CHOICES,
        label=" مدرک",
    )
    course = forms.ChoiceField(
        widget=forms.Select,
        choices=COURSE_CHOICES,
        label="درس ارائه شده",
    )
    classroom = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=CLASS_CHOICES,
        label="کلاس ها",
    )
    hire_date = forms.DateField(label="تاریخ استخدام")
    username = forms.CharField(max_length=255, label="نام کاربری")
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(), label="رمز عبور")


class NewCourse(forms.Form):
    name = forms.CharField(max_length=155, label="نام درس")


class NewClassRoom(forms.Form):
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
    level = forms.ChoiceField(widget=forms.Select, choices=LEVEL_CHOICES, label="پایه", )
    group = forms.ChoiceField(widget=forms.Select, choices=GROUP_CHOICES, label="گروه", )
    field = forms.ChoiceField(widget=forms.Select, choices=FIELD_CHOICES, label="رشته", )
