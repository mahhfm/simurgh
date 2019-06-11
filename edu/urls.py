from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [

    url(r'^$', views.home, name="home"),
    url(r'^apishow/$', views.api_show, name="api-show"),


    url(r'^data/', views.ShowData.as_view(), name="show-data"),
    url(r'^student/$', views.ModelCreateView.as_view(), name="student-signup"),
    url(r'^teacher/$', views.ModelCreateView.as_view(), name="new-teacher"),
    url(r'^course/$', views.ModelCreateView.as_view(), name="new-course"),
    url(r'^classroom/$', views.ModelCreateView.as_view(), name="new-class"),
    url(r'^register/$', views.ModelCreateView.as_view(), name="new-register"),
    url(r'^tcc/$', views.ModelCreateView.as_view(), name="new-tcc"),
    url(r'^parent/$', views.ModelCreateView.as_view(), name="new-parent"),
    url(r'^studentattendance/$', views.ModelCreateView.as_view(), name="new-studentattendance"),
    url(r'^teacherattendance/$', views.ModelCreateView.as_view(), name="new-teacherattendance"),
    url(r'^studentcourse/$', views.ModelCreateView.as_view(), name="new-studentcourse"),


    
    

    url(r'^student/(?P<pk>[0-9]+)/$', views.ShowDetail.as_view(), name="student-view"),
    url(r'^teacher/(?P<pk>[0-9]+)/$', views.ShowDetail.as_view(), name="teacher-view"),
    url(r'^course/(?P<pk>[0-9]+)/$', views.ShowDetail.as_view(), name="course-view"),
    url(r'^classroom/(?P<pk>[0-9]+)/$', views.ShowDetail.as_view(), name="classroom-view"),
    url(r'^register/(?P<pk>[0-9]+)/$', views.ShowDetail.as_view(), name="register-view"),
    url(r'^tcc/(?P<pk>[0-9]+)/$', views.ShowDetail.as_view(), name="tcc-view"),
    url(r'^parent/(?P<pk>[0-9]+)/$', views.ShowDetail.as_view(), name="parent-view"),
    url(r'^studentattendance/(?P<pk>[0-9]+)/$', views.ShowDetail.as_view(), name="studentattendance-view"),
    url(r'^teacherattendance/(?P<pk>[0-9]+)/$', views.ShowDetail.as_view(), name="teacherattendance-view"),
    url(r'^studentcourse/(?P<pk>[0-9]+)/$', views.ShowDetail.as_view(), name="studentcourse-view"),




    url(r'^student/update/(?P<pk>[0-9]+)/$', views.ModelUpdateView.as_view(), name="update-student"),
    url(r'^teacher/update/(?P<pk>[0-9]+)/$', views.ModelUpdateView.as_view(), name="update-teacher"),
    url(r'^classroom/update/(?P<pk>[0-9]+)/$', views.ModelUpdateView.as_view(), name="update-classroom"),
    url(r'^course/update/(?P<pk>[0-9]+)/$', views.ModelUpdateView.as_view(), name="update-course"),
    url(r'^register/update/(?P<pk>[0-9]+)/$', views.ModelUpdateView.as_view(), name="update-register"),
    url(r'^tcc/update/(?P<pk>[0-9]+)/$', views.ModelUpdateView.as_view(), name="update-tcc"),
    url(r'^parent/update/(?P<pk>[0-9]+)/$', views.ModelUpdateView.as_view(), name="update-parent"),
    url(r'^studentattendance/update/(?P<pk>[0-9]+)/$', views.ModelUpdateView.as_view(), name="update-studentattendance"),
    url(r'^teacherattendance/update/(?P<pk>[0-9]+)/$', views.ModelUpdateView.as_view(), name="update-teacherattendance"),
    url(r'^studentcourse/update/(?P<pk>[0-9]+)/$', views.ModelUpdateView.as_view(), name="update-studentcourse"),





    url(r'^student/delete/(?P<pk>[0-9]+)/$', views.DeleteModelView.as_view(), name="delete-student"),
    url(r'^course/delete/(?P<pk>[0-9]+)/$', views.DeleteModelView.as_view(), name="delete-course"),
    url(r'^classroom/delete/(?P<pk>[0-9]+)/$', views.DeleteModelView.as_view(), name="delete-classroom"),
    url(r'^teacher/delete/(?P<pk>[0-9]+)/$', views.DeleteModelView.as_view(), name="delete-teacher"),
    url(r'^register/delete/(?P<pk>[0-9]+)/$', views.DeleteModelView.as_view(), name="delete-register"),
    url(r'^tcc/delete/(?P<pk>[0-9]+)/$', views.DeleteModelView.as_view(), name="delete-tcc"),
    url(r'^parent/delete/(?P<pk>[0-9]+)/$', views.DeleteModelView.as_view(), name="delete-parent"),
    url(r'^studentattendance/delete/(?P<pk>[0-9]+)/$', views.DeleteModelView.as_view(), name="delete-studentattendance"),
    url(r'^teacherattendance/delete/(?P<pk>[0-9]+)/$', views.DeleteModelView.as_view(), name="delete-teacherattendance"),
    url(r'^studentcourse/delete/(?P<pk>[0-9]+)/$', views.DeleteModelView.as_view(), name="delete-studentcourse"),




    url(r'^login/',  views.LoginViewClass.as_view(), name="user-login"),
    url('^logout/', auth_views.LogoutView.as_view(template_name="edu/logout.html"), name="user-logout"),

    url(r'^salary/$', views.salary, name='salary'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)