from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
class TeacherSearchForm(forms.Form):
    BACHELOR, MA, PHD, ALL  = 'ba', 'ma', 'phd', 'all'
    DEGREE_CHOICES = (
        (ALL, "همه"),
        (BACHELOR, "لیسانس"),
        (MA, "فوق لیسانس"),
        (PHD, "دکتری"),
    )
    first_name = forms.CharField(max_length=20,required=False)
    last_name = forms.CharField(max_length=20,required=False)
    education_degree = forms.ChoiceField( required=False,choices=DEGREE_CHOICES,initial='')
    model_name = forms.CharField(max_length=20,widget=forms.HiddenInput(),initial='teacher')

class StudentSearchForm(forms.Form):
    first_name = forms.CharField(max_length=20,required=False)
    last_name = forms.CharField(max_length=20,required=False)
    model_name = forms.CharField(max_length=20,widget=forms.HiddenInput(),initial='student')

class TeacherForm(forms.ModelForm):
    username = forms.CharField(max_length=155, label='نام کاربری')
    first_name = forms.CharField(max_length=155, label='نام')
    last_name = forms.CharField(max_length=155, label='نام خانوادگی')
    email = forms.EmailField(max_length=155, label='ایمیل')
    password = forms.CharField(widget=forms.PasswordInput, label='رمزعبور')
    re_password = forms.CharField(widget=forms.PasswordInput, label='تکرار رمزرعبور')
    def clean(self):
        data = self.cleaned_data
        print(self.cleaned_data)
        pass1 = data.get('password')
        pass2 = data.get('re_password')
        if pass1 != pass2:
            raise forms.ValidationError('رمز عبور یکسان نیست')
        return data     
    class Meta:
        model = Teacher
        exclude = ('classroom','user','profession','tid' )

class ClassRoomForm(forms.ModelForm):
    class Meta:
        model = ClassRoom
        fields = '__all__'

class TCCForm(forms.ModelForm):
    class Meta:
        model = TCC
        fields = '__all__'

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
class RegisterForm(forms.ModelForm):
    def form_valid(self):
        print("This is save test")
    class Meta:
        model = Register
        fields = '__all__'
        # fields=['student','classroom','active']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class StudentAttendanceForm(forms.ModelForm):
    # def __init__(self,user, *args, **kwargs):
    #     super(StudentAttendanceForm, self).__init__(*args, **kwargs)
    #     self.fields['register'] = forms.ChoiceField(
    #         choices=[(o.id, str(o.classroom)) for o in Register.objects.filter(student__user__username=user)]
    #     )
    class Meta:
        model = StudentAttendance
        fields = '__all__'


class TeacherAttendanceForm(forms.ModelForm):
    class Meta:
        model = TeacherAttendance
        fields = '__all__'


class ParentForm(forms.ModelForm):
    username = forms.CharField(max_length=155, label='نام کاربری')
    first_name = forms.CharField(max_length=155, label='نام')
    last_name = forms.CharField(max_length=155, label='نام خانوادگی')
    email = forms.EmailField(max_length=155, label='ایمیل')
    password = forms.CharField(widget=forms.PasswordInput, label='رمزعبور')
    re_password = forms.CharField(widget=forms.PasswordInput, label='تکرار رمزرعبور')
    def clean(self):
        data = self.cleaned_data
        print(self.cleaned_data)
        pass1 = data.get('password')
        pass2 = data.get('re_password')
        if pass1 != pass2:
            raise forms.ValidationError('رمز عبور یکسان نیست')
        return data     
    class Meta:
        model = Parent
        exclude =  ('user',)

class StudentForm(forms.ModelForm):
    username = forms.CharField(max_length=155, label='نام کاربری')
    first_name = forms.CharField(max_length=155, label='نام')
    last_name = forms.CharField(max_length=155, label='نام خانوادگی')
    email = forms.EmailField(max_length=155, label='ایمیل')
    password = forms.CharField(widget=forms.PasswordInput, label='رمزعبور')
    re_password = forms.CharField(widget=forms.PasswordInput, label='تکرار رمزرعبور')
    def clean(self):
        data = self.cleaned_data
        print(self.cleaned_data)
        pass1 = data.get('password')
        pass2 = data.get('re_password')
        if pass1 != pass2:
            raise forms.ValidationError('رمز عبور یکسان نیست')
        return data 

    class Meta:
        model = Student
        exclude = ( 'sid','classroom', 'courses', 'user')

        
class StudentCourseForm(forms.ModelForm):
    class Meta:
        model = StudentCourse
        fields = '__all__'


class Salary(forms.Form):
    teach_code = forms.CharField(max_length=12, label="لطفا کد پرسنلی خود را وارد کنید")
    username = forms.CharField(max_length=32, label="نام کاربری")

    def clean(self):
        code = self.cleaned_data.get('teach_code')
        username = self.cleaned_data.get('username')

        this_user = User.objects.filter(username=username).first()
        teacher = Teacher.objects.filter(user=this_user, tid=code).first()
        if teacher:
            pass
        else:
            raise forms.ValidationError('اطلاعاتی با این مشخصات وجود ندارد')

#     # first_name = forms.CharField(max_length=55)
#     # last_name = forms.CharField(max_length=55)
#     class Meta:
#         model = Student

#         fields = "__all__"
#         exclude = ['user', 'sid']

#         labels = {
#             'classroom': 'کلاس',
#             'courses': 'دروس',
#         }

#     def clean(self):
#         data = self.cleaned_data
#         pass1 = data.get('pass1')
#         pass2 = data.get('pass2')

#         if pass1 != pass2:
#             raise forms.ValidationError('رمز عبور یکسان نیست')

#         return data

# class NewStudent(forms.Form):
#     LEVEL_CHOICES = [
#         ("7", "هفتم"),
#         ("8", "هشتم"),
#         ("9", "نهم"),
#         ("10", "دهم"),
#         ("11", "یازدهم"),
#         ("12", "دوازدهم"),
#     ]
#
#     GROUP_CHOICES = (
#         ("a", "الف"),
#         ("b", "ب"),
#         ("c", "ج")
#     )
#
#     FIELD_CHOICES = (
#         ("ms", "ریاضی"),
#         ("es", "تجربی"),
#         ("hs", "انسانی")
#     )
#
#     name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-group'}), label="نام")
#     family = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-group'}),
#                              label="نام خانوادگی")
#     email = forms.EmailField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-group'}), label="ایمیل ")
#     level = forms.ChoiceField(choices=LEVEL_CHOICES, widget=forms.Select(attrs={'class': 'form-group'}),
#                               label="پایه")
#     group = forms.ChoiceField(choices=GROUP_CHOICES, widget=forms.Select(attrs={'class': 'form-group'}), label=" گروه")
#     field = forms.ChoiceField(choices=FIELD_CHOICES, widget=forms.Select(attrs={'class': 'form-group'}), label="رشته ")
#     username = forms.CharField(max_length=255, label="نام کاربری")
#     password = forms.CharField(max_length=32, widget=forms.PasswordInput(), label="رمز عبور")
#     confirm_password = forms.CharField(max_length=32, widget=forms.PasswordInput(), label="تایید عبور")
#
#     def clean(self):
#         data = self.cleaned_data
#         pass1 = data.get('password')
#         pass2 = data.get('confirm_password')
#
#         if pass1 != pass2:
#             raise forms.ValidationError(
#                 'رمز عبور یکسان نیست'
#             )
#
#
# class NewTeacher(forms.Form):
#     CLASS_CHOICES = [[cls.id, cls.__str__()] for cls in ClassRoom.objects.all()]
#     COURSE_CHOICES = [[course.id, course.course_name] for course in Course.objects.all()]
#
#     BACHELOR, MA, PHD = 'ba', 'ma', 'phd'
#     DEGREE_CHOICES = (
#         (BACHELOR, "لیسانس"),
#         (MA, "فوق لیسانس"),
#         (PHD, "دکتری"),
#     )
#
#     name = forms.CharField(max_length=255, label="نام")
#     family = forms.CharField(max_length=255, label="نام خانوادگی")
#     email = forms.EmailField(max_length=255, label="ایمیل ")
#     education_degree = forms.ChoiceField(
#         widget=forms.Select,
#         choices=DEGREE_CHOICES,
#         label=" مدرک",
#     )
#     course = forms.ChoiceField(
#         widget=forms.Select,
#         choices=COURSE_CHOICES,
#         label="درس ارائه شده",
#     )
#     classroom = forms.MultipleChoiceField(
#         widget=forms.CheckboxSelectMultiple,
#         choices=CLASS_CHOICES,
#         label="کلاس ها",
#     )
#     hire_date = forms.DateField(label="تاریخ استخدام")
#     username = forms.CharField(max_length=255, label="نام کاربری")
#     password = forms.CharField(max_length=32, widget=forms.PasswordInput(), label="رمز عبور")
#     confirm_password = forms.CharField(max_length=32, widget=forms.PasswordInput(), label="تایید عبور")
#
#     def clean(self):
#         data = self.cleaned_data
#         pass1 = data.get('password')
#         pass2 = data.get('confirm_password')
#
#         if pass1 != pass2:
#             raise forms.ValidationError(
#                 'رمز عبور یکسان نیست'
#             )
#
#
# class NewCourse(forms.Form):
#     name = forms.CharField(max_length=155, label="نام درس")
#
#
# class NewClassRoom(forms.Form):
#     MS, ES, HS = 'ms', 'es', 'hs'
#     FIELD_CHOICES = (
#         (MS, "ریاضی"),
#         (ES, "تجربی"),
#         (HS, "انسانی")
#     )
#
#     A, B, C = 'a', 'b', 'c'
#     GROUP_CHOICES = (
#         (A, "الف"),
#         (B, "ب"),
#         (C, "ج")
#     )
#
#     L7, L8, L9, L10, L11, L12 = '7', '8', '9', '10', '11', '12'
#     LEVEL_CHOICES = (
#         (L7, "هفتم"),
#         (L8, "هشتم"),
#         (L9, "نهم"),
#         (L10, "دهم"),
#         (L11, "یازدهم"),
#         (L12, "دوازدهم"),
#     )
#     level = forms.ChoiceField(widget=forms.Select, choices=LEVEL_CHOICES, label="پایه", )
#     group = forms.ChoiceField(widget=forms.Select, choices=GROUP_CHOICES, label="گروه", )
#     field = forms.ChoiceField(widget=forms.Select, choices=FIELD_CHOICES, label="رشته", )
