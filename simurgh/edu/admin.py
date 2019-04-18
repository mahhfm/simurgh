from django.contrib import admin
from .models import Course, Student, Teacher, ClassRoom



class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'hire_date', 'profession', 'tid', 'experiences')
    list_display_links = ('user', 'hire_date', 'profession', 'tid', 'experiences')
    search_fields = ['user__username']
    list_filter = ('hire_date', 'profession', 'classroom')



class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'classroom', 'sid')
    list_display_links = ('user', 'classroom')

    list_filter =  ('classroom',)

admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Course)
admin.site.register(ClassRoom)