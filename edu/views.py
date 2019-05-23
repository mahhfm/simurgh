from django.shortcuts import render, get_object_or_404
from random import randint
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Teacher, ClassRoom, Student, Course, Register, TCC
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
        if self.request.user.groups.all().first().name == 'manager_management':
            return super().dispatch(*args, **kwargs)
        return render(self.request, 'edu/not_allowed.html')

    def sid(self):
        code = ''
        from random import randint
        for _ in range(15):
            code += str(randint(0, 9))

        return code

    def form_valid(self, form):
        if  'student' in self.request.path :
            data = form.cleaned_data
            new_user = User.objects.create(
                username=data.pop('username'),
                first_name=data.pop('first_name'),
                last_name=data.pop('last_name'),
                email=data.pop('email'),
                password=make_password(data.pop('password')),
            )
            data.pop('re_password'),
            new_student = form.save(commit=False)
            new_student.user = new_user
            new_student.sid = get_student_code()
            new_student.save()
            group = Group.objects.get(name='student_management')
            group.user_set.add(new_student.user)
            group.save()
        if 'teacher' in self.request.path:
            data = form.cleaned_data
            new_user = User.objects.create(
                username=data.pop('username'),
                first_name=data.pop('first_name'),
                last_name=data.pop('last_name'),
                email=data.pop('email'),
                password=make_password(data.pop('password')),
            )
            data.pop('re_password'),
            new_student = form.save(commit=False)
            new_student.user = new_user
            new_student.tid = get_student_code()
            new_student.save()
            group = Group.objects.get(name='teacher_management')
            group.user_set.add(new_student.user)
            group.save()
        super().form_valid(form)
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
        print(self.request)
        form_request = {
            'student': StudentForm,
            'teacher': TeacherForm,
            'classroom': ClassRoomForm,
            'course': CourseForm,
            'register':RegisterForm,
            'tcc': TCCForm, }

        form_class = form_request[self.request.path.strip('/')]
        print(form_class)
        return form_class(**self.get_form_kwargs())


class ShowData(ListView):
    template_name = 'edu/show_data.html'
    model = Student


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.groups.all().first().name == 'manager_management' or self.request.user.groups.all().first().name == 'teacher_management':
            return super().dispatch(*args, **kwargs)
        return render(self.request, 'edu/not_allowed.html')
    
    def get_context_data(self, **kwargs):
        context = super(ShowData, self).get_context_data(**kwargs)
        format_request = {
            'student': Student,
             'teacher': Teacher,
             'classroom': ClassRoom,
             'course': Course,
             'register':Register,
             'tcc' : TCC,
            }
        search_request = {
            'teacher': TeacherSearchForm,
            'student': StudentSearchForm,
            'classroom': None,
             'course': None,
             'register':None,
             'tcc' : None,

            }
        try:
            if self.request.GET.get('model_name'):
                model_name = self.request.GET.get('model_name')
                first_name = self.request.GET.get('first_name')
                last_name = self.request.GET.get('last_name')
                if 'teacher' in model_name :
                    education_degree = self.request.GET.get('education_degree')
                    filter_search=Teacher.objects.filter(Q(user__first_name__icontains= first_name) & Q(user__last_name__icontains= last_name) & Q(education_degree= education_degree) )
                    if  self.request.GET.get('education_degree') == 'all':
                        filter_search=Teacher.objects.filter(Q(user__first_name__icontains= first_name) & Q(user__last_name__icontains= last_name))
                else:
                    filter_search=Student.objects.filter(Q(user__first_name__icontains= first_name) & Q(user__last_name__icontains= last_name))
                self.model = format_request[model_name]
                context.update({
                str(model_name) + 's': filter_search ,
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
            'tcc':TCC,
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
            'register':Register,
             'tcc':TCC,
              }
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
            'register':Register, 
            'tcc':TCC}
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


def get_student_code():
    code =''
    for _ in range(5):
        code += str(randint(0, 9))
    
    return int(code)