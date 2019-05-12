from rest_framework import serializers
from .models import Student 
from django.contrib.auth.models import User 
from django.contrib.auth.hashers import make_password 

class LevelFieldSerializer(serializers.Serializer):
    field = serializers.CharField()
    level = serializers.CharField()

class ClassRoomSerializer(serializers.Serializer):
    branch = serializers.CharField()
    education_year = serializers.CharField()
    level_field = LevelFieldSerializer()    

class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()


class CourseSerializer(serializers.Serializer):
    course_name = serializers.CharField()
    unite = serializers.IntegerField()
    level_field = LevelFieldSerializer() 



class StudentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user=UserSerializer()
    sid = serializers.IntegerField()
    courses= CourseSerializer(many=True)
    classroom= ClassRoomSerializer(many=True)
    

    def create(self, validated_data):

        user_instance = User(
                username=self.validated_data['user'],
                first_name= self.validated_data['first_name'],
                password=make_password(self.validated_data['password']),

                 )
        user_instance.save()
        return Student.objects.create(user = user_instance ,sid =  self.validated_data['sid'])


# =========================================================Shell Commands ==================================
# from edu.models import Student
# from edu.serializers import StudentSerializer
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser


# student = Student(sid='12434534534', user='jadmin' , password = 'jadmin123123123') 
# student.save()



# data={'sid':'879846598', 'user':'jadmin78' , 'password' : 'jadmin123123123', 'first_name':'ABBBASSS'}
# serializer = StudentSerializer(data=data)
# serializer.data



