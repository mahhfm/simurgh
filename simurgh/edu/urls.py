from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name="home"),
    # url(r'^class/list/(?P<id>\w+)/$', views.class_list, name="class-list"),
    url(r'^data/', views.show_data, name="show-data"),
    url(r'^newstudent/', views.new_student, name="new-student"),
    url(r'^newteacher/', views.new_teacher, name="new-teacher"),
    url(r'^newcourse/', views.new_course, name="new-course"),
    url(r'^newclass/', views.new_classroom, name="new-class"),
]
