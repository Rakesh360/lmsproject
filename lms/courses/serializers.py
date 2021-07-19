
from rest_framework import serializers
from base_rest.utils import *
from .models import *

class LessonsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        exclude = ['created_at', 'updated_at']


class CourseChaptersSerializers(serializers.ModelSerializer):
    course_lessons = LessonsSerializers(source ="course_chapters" , many=True)
    class Meta:
        model = SubjectChapters
        exclude = ['created_at', 'updated_at']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        exclude = ['created_at' , 'updated_at']


class SubjectChaptersSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(source ='course_chapters' , many =True)
    class Meta:
        model = SubjectChapters
        exclude = ['created_at' , 'updated_at']


class SubjectSerializer(serializers.ModelSerializer):
    chapters = SubjectChaptersSerializer(source ="subject" , many=True)
    class Meta:
        model = Subject
        fields = ['subject_title' , 'chapters']




class CourseSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True)
    course_package_info = serializers.SerializerMethodField()
    class Meta:
        model = CoursePackage
    
        fields = '__all__'
        depth = 1

    def get_course_package_info(self,obj):
        print(obj)
        import json
        return json.loads(obj.course_package_info)


