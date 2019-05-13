# from django.contrib.contenttypes.models import ContentType
# from django.contrib.auth.models import Permission, User
# from django.shortcuts import get_object_or_404
# from .models import *

# {% if perms.app_label.can_do_something %}
# <form here>
# {% endif %}





# from myapp.models import BlogPost
# from django.contrib.auth.models import Permission
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.auth.models import Permission, User
# from django.shortcuts import get_object_or_404
# from edu.models import *

# content_type = ContentType.objects.get_for_model(Student)
# permission = Permission.objects.create(codename='view_student',
#                                        name='View Students',
#                                        content_type=content_type)

# user= Student.user.get_queryset()
# user = get_object_or_404(User, pk=4)
# user= Student.objects.all()
# permission = Permission.objects.get(codename='view_student')
# user.user_permissions.add(permission)

# user.has_perm('edu.view_student')