from django.shortcuts import render, get_object_or_404
from random import randint
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Teacher, ClassRoom, Student, Course, Register
from django.urls import reverse_lazy
from .forms import *
from django.http import HttpResponseRedirect, HttpResponse
import jdatetime
import persian
from dateutil.relativedelta import relativedelta
from datetime import date
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    # DeleteView,
)
from django.views.generic.edit import DeleteView
from rest_framework import routers, serializers, viewsets
from rest_framework import serializers
from .models import Student 
from django.contrib.auth.models import User 
from django.contrib.auth.hashers import make_password 
from edu.models import Student
from edu.serializers import StudentSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView


def home(request):
    return render(request, 'edu/base.html')


class ModelCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'edu/new.html'
    success_url = '/student/'


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ModelCreateView, self).dispatch(*args, **kwargs)

    def sid(self):
        code = ''
        from random import randint
        for _ in range(15):
            code += str(randint(0, 9))

        return code

    def form_valid(self, form):
        add_student = form.save(commit=False)
        add_student.user = self.request.user
        add_student.sid = self.sid()
        add_student.save()
        return render(self.request, self.template_name, context={'create_message': 'با موفقیت اضافه شد '})
        # return HttpResponseRedirect(self.get_success_url())
        # return super().form_valid(form)
        # add_student = form.save(commit=False)
        # add_student.user = self.request.user
        # for key in ['first_name', 'last_name']:
        #     setattr(self.request.user, key, form.cleaned_data.get(key))
        # self.request.user.save()
        # return super(StudentCreateView, self).form_valid(form)

    def get_form(self, form_class=None):
        form_request = {
            'student': StudentForm,
            'teacher': TeacherForm,
            'classroom': ClassRoomForm,
            'course': CourseForm,
            'register':Register, }

        form_class = form_request[self.request.path.strip('/')]
        return form_class(**self.get_form_kwargs())


class ShowData(ListView):
    template_name = 'edu/show_data.html'
    model = Student


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(ShowData, self).get_context_data(**kwargs)
        format_request = {
            'student': Student,
             'teacher': Teacher,
             'classroom': ClassRoom,
             'course': Course,
             'register':Register,
            }
        search_request = {
            'teacher': TeacherSearchForm,
            'student': StudentSearchForm,
            'classroom': None,
             'course': None,
             'register':None,

            }
        try:
            if self.request.GET.get('model_name'):
                model_name = self.request.GET.get('model_name')
                first_name = self.request.GET.get('first_name')
                last_name = self.request.GET.get('last_name')
                if 'teacher' in model_name :
                    education_degree = self.request.GET.get('education_degree')
                    education_degree=Q(education_degree= education_degree)
                    if  self.request.GET.get('education_degree') == 'all':
                        education_degree= ~Q()
                else:
                    education_degree = None
                print(education_degree)
                self.model = format_request[model_name]
                context.update({
                str(model_name) + 's': self.model.objects.filter(Q(user__first_name__icontains= first_name) & Q(user__last_name__icontains= last_name) &  education_degree ),
                'search': search_request[model_name],
                 })
            else:
                model_name = [key for key in dict(self.request.GET)][0]

                self.model = format_request[model_name]             
                context.update({
                    str(model_name) + 's': self.model.objects.all(),
                    'search': search_request[model_name] ,
                })

        except IndexError:
            context.update({
                'Errors': "There is No Records",
            })
        return context




class ShowDetail(DetailView):
    template_name = 'edu/show_data.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        model_name = self.request.path[1: self.request.path.index('/', 1)]
        format_request = {
            'student': Student,
            'teacher': Teacher,
            'course': Course,
            'classroom': ClassRoom,
            'register':Register,
        }

        self.model = format_request[model_name]
        queryset = super(ShowDetail, self).get_queryset()
        return queryset.all()


class ModelUpdateView(UpdateView):
    fields = "__all__"
    template_name = "edu/update.html"
    path_name = ''

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        list_model = {
            'student': Student,
            'teacher': Teacher,
            'classroom': ClassRoom,
            'course': Course,
            'register':Register, }
        self.model = list_model[self.request.path[1:self.request.path.index('/', 1)]]
        self.path_name = self.request.path[1:self.request.path.index('/', 1)]
        queryset = super(ModelUpdateView, self).get_queryset()
        return queryset.all()

    def form_valid(self, form):
        update_student = form.save(commit=False)
        update_student.save()
        print(self.path_name)
        return render(self.request, 'edu/show_data.html', context={self.path_name + 's': self.model.objects.all(),
                                                                   'update_message': 'با موفقیت آپدیت شد '})


class DeleteModelView(DeleteView):
    model = Course
    template_name = 'edu/delete_object.html'
    success_url = ''
    path_name = ''

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        list_model = {
            'student': Student,
            'teacher': Teacher,
            'classroom': ClassRoom,
            'course': Course,
            'register':Register, }
        self.model = list_model[self.request.path[1:self.request.path.index('/', 1)]]
        self.success_url = '/data/?' + self.request.path[1:self.request.path.index('/', 1)] + '='
        self.path_name = self.request.path[1:self.request.path.index('/', 1)]
        queryset = super(DeleteModelView, self).get_queryset()
        return queryset.all()




class LoginViewClass(LoginView):
    template_name="edu/login.html"




def api_show(request):
    list_of_ser={}
    for student in Student.objects.all():
        list_of_ser[student.user.username] = StudentSerializer(student).data
    return JsonResponse(list_of_ser)
    # return HttpResponse(StudentSerializer(Student.objects.all(), many=True).data)





######################################  class base view ####################################
# def student_signup(request):
#     form = StudentForm()
#     if request.method == 'POST':
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             print(form)
#             print(form.cleaned_data)
#             # student = form.save(commit=False)
#             # student.sid = get_sid()
#             # student.save()
#
#         else:
#             return render(request, 'edu/new.html', {'StudentForm': form})
#     else:
#         user = User.objects.filter(username=request.user).first()
#         print(user)
#         # form = StudentForm(instance=)
#         return render(request, 'edu/new.html', {'StudentForm': form})


def get_date_time():
    now = jdatetime.datetime.now()
    datetime, time = str(now).split()
    time = time[:5]
    year, month, day = datetime.split('-')
    year, month, day = persian.enToPersianNumb(year), persian.enToPersianNumb(month), persian.enToPersianNumb(day)
    hour, minute = time.split(":")
    hour, minute = persian.enToPersianNumb(hour), persian.enToPersianNumb(minute)
    datetime = day + '-' + month + '-' + year  # i change day and year to show in true format
    time = hour + ':' + minute

    return f"امروز {datetime} ساعت {time}"


def show_data(request):
    if 'student' in request.GET:
        return render(request, 'edu/show_data.html',
                      context={'students': Student.objects.all(), 'date': get_date_time()})
    elif 'teacher' in request.GET:
        teachers = []
        for teacher in Teacher.objects.all():
            new_teacher_add = dict(
                id=teacher.id,
                name=teacher.user.first_name,
                family=teacher.user.last_name,
                code=teacher.tid,
                experience=teacher.experience,
                email=teacher.user.email,
                classes=",".join(cls.__str__() for cls in teacher.classroom.all()),
            )
            teachers.append(new_teacher_add)

        return render(request, 'edu/show_data.html', context={'teachers': teachers, 'date': get_date_time()})
    elif 'course' in request.GET:
        return render(request, 'edu/show_data.html', context={'courses': Course.objects.all(), 'date': get_date_time()})
    elif 'classroom' in request.GET:
        return render(request, 'edu/show_data.html',
                      context={'order_classrooms': ClassRoom.objects.order_by('field'), 'date': get_date_time()})


def get_student_code():
    sid = '98'
    for _ in range(10):
        sid += str(randint(1, 9))

    return int(sid)


def new_student(request):
    form = NewStudent
    if request.method == "POST":
        form = NewStudent(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            c = ClassRoom.objects.get_or_create(
                level=data.get('level'),
                group=data.get('group'),
                field=data.get('field'),
            )[0]

            user = User.objects.create(
                username=data.get('username'),
                password=make_password(data.get('password')),
                first_name=data.get('name'),
                last_name=data.get('family'),
                email=data.get('email'),
            )
            user.save()

            s = Student.objects.create(
                user=user,
                classroom=c,
                sid=get_student_code(),
            )
            s.save()

            return render(request, 'edu/base.html', context={'msg': f"{s} اضافه شد به {c}", 'date': get_date_time()})
        else:
            return render(request, 'edu/new.html',
                          context={'StudentForm': form, 'classrooms': ClassRoom.objects.all(), 'date': get_date_time()})
    else:
        return render(request, 'edu/new.html',
                      context={'StudentForm': form, 'classrooms': ClassRoom.objects.all(), 'date': get_date_time()})


def get_teacher_code():
    code = '9830'
    for _ in range(8):
        code += str(randint(0, 9))

    return code


def new_teacher(request):
    form = NewTeacher()
    if request.method == 'POST':
        form = NewTeacher(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            classes_objects = [ClassRoom.objects.filter(id=id).first() for id in data.get('classroom')]
            user = User.objects.create(
                username=data.get('username'),
                password=make_password(data.get('password')),
                first_name=data.get('name'),
                last_name=data.get('family'),
                email=data.get('email'),
            )
            user.save()
            t = Teacher.objects.create(
                user=user,
                hire_date=data.get('hire_date'),
                education_degree=data.get('education_degree'),
                profession=Course.objects.filter(id=data.get('course')).first(),
                tid=get_teacher_code(),
            )
            t.save()
            for chosen_class in classes_objects:
                t.classroom.add(chosen_class)
                t.save()
            return render(request, 'edu/base.html',
                          context={'msg': f"{user.first_name + ' ' + user.last_name} اضافه شد به معلمین ",
                                   'date': get_date_time()})
        else:
            return render(request, 'edu/new.html',
                          context={'TeacherForm': form, 'teachers': Teacher.objects.all(), 'date': get_date_time()})
    else:
        return render(request, 'edu/new.html',
                      context={'TeacherForm': form, 'teachers': Teacher.objects.all(), 'date': get_date_time()})


def new_course(request):
    form = NewCourse()
    if request.method == "POST":
        form = NewCourse(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_course_add = Course.objects.get_or_create(
                course_name=data.get('name'),
            )[0]
            return render(request, 'edu/base.html',
                          context={'msg': new_course_add.__str__() + " اکنون موجود است ", 'date': get_date_time()})
        else:
            return render(request, 'edu/new.html',
                          context={'CourseForm': form, 'courses': Course.objects.all(), 'date': get_date_time()})
    else:
        return render(request, 'edu/new.html',
                      context={'CourseForm': form, 'courses': Course.objects.all(), 'date': get_date_time()})


def new_classroom(request):
    form = NewClassRoom()
    if request.method == 'POST':
        form = NewClassRoom(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_class_room = ClassRoom.objects.get_or_create(
                level=data.get('level'),
                group=data.get('group'),
                field=data.get('field')
            )[0]
            return render(request, 'edu/base.html',
                          context={'msg': new_class_room.__str__() + ' اکنون موجود است', 'date': get_date_time()})
        else:
            return render(request, 'edu/new.html',
                          context={'ClassFrom': form, 'classrooms': ClassRoom.objects.all(), 'date': get_date_time()})
    else:
        return render(request, 'edu/new.html',
                      context={'ClassFrom': form, 'classrooms': ClassRoom.objects.all(), 'date': get_date_time()})


@login_required(login_url='/login/')
def salary(request):
    form = Salary()
    if request.method == 'POST':
        form = Salary(request.POST)
        if form.is_valid():
            earn = 0
            degree_additional = {
                'ba': 1000000,
                'ma': 1500000,
                'phd': 2400000,
            }

            degree_format = {
                'ba': 'لیسانس',
                'ma': 'فوق لیسانس',
                'phd': 'دکنری',
            }
            code = form.cleaned_data.get('teach_code')
            teacher = Teacher.objects.filter(tid=code).first()
            delta = relativedelta(date.today(), teacher.hire_date)
            days = (delta.years * 365) + (delta.months * 30) + delta.days
            earn = (earn + days * 15000) + degree_additional[teacher.education_degree]
            teacher_info = dict(
                id=teacher.id,
                full_name=teacher.user.first_name + " " + teacher.user.last_name,
                degree=degree_format[teacher.education_degree],
                experience=teacher.experience,
                earn=persian.enToPersianNumb(f"{earn:,}"),
            )

            return render(request, 'edu/salary.html', context={'result': teacher_info, 'date': get_date_time()})
        else:
            return render(request, 'edu/salary.html', context={'form': form, 'date': get_date_time()})
    else:
        return render(request, 'edu/salary.html',
                      context={'form': form, 'date': get_date_time(), 'msg': 'برای دسترسی باید وارد شوید'})
