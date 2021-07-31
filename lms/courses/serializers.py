
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
    lessons = LessonSerializer(source ='subject_lessons' , many =True)
    class Meta:
        model = SubjectChapters
        exclude = ['created_at' , 'updated_at']


class SubjectSerializer(serializers.ModelSerializer):
    #chapters = SubjectChaptersSerializer(source ="subject_chapters" , many=True)
    class Meta:
        model = Subject
        exclude = ['created_at' , 'updated_at']


class CoursePackageLessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursePackageLessons
        exclude = ['created_at' , 'updated_at']
       

class CoursePackageChaptersSerializer(serializers.ModelSerializer):
    lessons = CoursePackageLessonsSerializer(source ='pacakge_subject_chapters_lessons' , many =True)
    
    class Meta:
        model = CoursePackageChapters
        exclude = ['created_at' , 'updated_at']
       
class CoursePackageSubjectsSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    chapters = CoursePackageChaptersSerializer(source ='pacakge_subject_chapters' , many =True)
    class Meta:
        model = CoursePackageSubjects
        exclude = ['created_at' , 'updated_at']
       

class CourseSerializer(serializers.ModelSerializer):
    #course_package_info = serializers.SerializerMethodField()
    subjects = CoursePackageSubjectsSerializer(source ="pacakge_subjects" , many=True)

    class Meta:
        model = CoursePackage
    
        exclude = ['created_at' , 'updated_at']

        depth = 1

    # def get_course_package_info(self,obj):
    #     print(obj)
    #     import json
    #     return json.loads(obj.course_package_info)


