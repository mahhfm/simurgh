from django.shortcuts import render
from django.http import HttpResponse
from random import randint
from django.contrib.auth.models import User

from .models import Teacher, ClassRoom, Student, Course
from .forms import NewStudent, NewTeacher, NewCourse, NewClassRoom


def home(request):
    return render(request, 'edu/base.html')


def show_data(request):
    if 'student' in request.GET:
        return render(request, 'edu/show_data.html', context={'students': Student.objects.all()})
    elif 'teacher' in request.GET:
        return render(request, 'edu/show_data.html', context={'teachers': Teacher.objects.all()})
    elif 'course' in request.GET:
        return render(request, 'edu/show_data.html', context={'courses': Course.objects.all()})
    elif 'classroom' in request.GET:
        return render(request, 'edu/show_data.html',
                      context={'order_classrooms': ClassRoom.objects.order_by('field')})


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
                password=data.get('password'),
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

            return render(request, 'edu/base.html', context={'msg': f"{s} اضافه شد به {c}"})
        else:
            return HttpResponse("{'status': 'invalid'}")
    else:
        return render(request, 'edu/new.html', context={'StudentForm': form, 'classrooms': ClassRoom.objects.all()})


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
                password=data.get('password'),
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
            for cls in classes_objects:
                t.classroom.add(cls)
                t.save()
            return render(request, 'edu/base.html',
                          context={'msg': f"{user.first_name + ' ' + user.last_name} اضافه شد به معلمین "})

    else:
        return render(request, 'edu/new.html', context={'TeacherForm': form, 'teachers': Teacher.objects.all()})


def new_course(request):
    form = NewCourse()
    if request.method == "POST":
        form = NewCourse(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            course_name = data.get('name')
            course = Course.objects.get_or_create(course_name=course_name)
            return render(request, 'edu/base.html', context={'msg': f"{course_name} اضافه شد"})

    else:
        return render(request, 'edu/new.html', context={'CourseForm': form, 'courses': Course.objects.all()})


def new_classroom(request):
    form = NewClassRoom()
    if request.method == 'POST':
        pass
    else:
        return render(request, 'edu/new.html', context={'ClassFrom': form, 'classrooms': ClassRoom.objects.all()})
