from django.contrib import admin
from . import models



# class TeacherAdmin(admin.ModelAdmin):
#     list_display = ('user', 'hire_date', 'profession', 'tid', 'experiences')
#     list_display_links = ('user', 'hire_date', 'profession', 'tid', 'experiences')
#     search_fields = ['user__username']
#     list_filter = ('hire_date', 'profession', 'classroom')
#
#
#
# class StudentAdmin(admin.ModelAdmin):
#     list_display = ('user', 'classroom', 'sid')
#     list_display_links = ('user', 'classroom')
#
#     list_filter =  ('classroom',)
#


admin.site.register(models.Student)
admin.site.register(models.Teacher)
admin.site.register(models.Course)
admin.site.register(models.ClassRoom)
admin.site.register(models.LevelField)
admin.site.register(models.StudentCourse)
admin.site.register(models.Register)
admin.site.register(models.TCC)
