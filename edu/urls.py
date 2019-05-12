from django.conf.urls import url, include
from . import views

urlpatterns = [

    url(r'^$', views.home, name="home"),
    url(r'^apishow/$', views.api_show, name="api-show"),


    url(r'^data/$', views.ShowData.as_view(), name="show-data"),
    url(r'^student/$', views.ModelCreateView.as_view(), name="student-signup"),
    url(r'^teacher/$', views.ModelCreateView.as_view(), name="new-teacher"),
    url(r'^course/$', views.ModelCreateView.as_view(), name="new-course"),
    url(r'^classroom/$', views.ModelCreateView.as_view(), name="new-class"),


    url(r'^student/(?P<pk>[0-9]+)/$', views.ShowDetail.as_view(), name="student-view"),
    url(r'^teacher/(?P<pk>[0-9]+)/$', views.ShowDetail.as_view(), name="teacher-view"),
    url(r'^course/(?P<pk>[0-9]+)/$', views.ShowDetail.as_view(), name="course-view"),
    url(r'^classroom/(?P<pk>[0-9]+)/$', views.ShowDetail.as_view(), name="classroom-view"),


    url(r'^student/update/(?P<pk>[0-9]+)/$', views.ModelUpdateView.as_view(), name="update-student"),
    url(r'^teacher/update/(?P<pk>[0-9]+)/$', views.ModelUpdateView.as_view(), name="update-teacher"),
    url(r'^classroom/update/(?P<pk>[0-9]+)/$', views.ModelUpdateView.as_view(), name="update-classroom"),
    url(r'^course/update/(?P<pk>[0-9]+)/$', views.ModelUpdateView.as_view(), name="update-course"),


    url(r'^student/delete/(?P<pk>[0-9]+)/$', views.DeleteModelView.as_view(), name="delete-student"),
    url(r'^course/delete/(?P<pk>[0-9]+)/$', views.DeleteModelView.as_view(), name="delete-course"),
    url(r'^classroom/delete/(?P<pk>[0-9]+)/$', views.DeleteModelView.as_view(), name="delete-classroom"),
    url(r'^teacher/delete/(?P<pk>[0-9]+)/$', views.DeleteModelView.as_view(), name="delete-teacher"),


    url(r'^salary/$', views.salary, name='salary'),
]
