
from django.contrib.auth import models
from django.db.models import fields
from accounts.models import Student
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
import uuid
from base_rest.utils import *
from .models import *


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['category_name' ,'category_image']

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
    subject_category = CourseCategorySerializer()
    chapters = SubjectChaptersSerializer(source ="subject" , many=True)
    class Meta:
        model = Subject
        fields = ['subject_category','subject_title' , 'chapters']




class CourseSerializer(serializers.ModelSerializer):
    course_bundle_category = CourseCategorySerializer()
    subjects = SubjectSerializer(many=True)
    class Meta:
        model = Course
    
        fields = [
        'uid',
        'course_bundle_category',
        'course_bundle_price',
        'course_bundle_discount',
        'course_bundle_image',
        'course_bundle_description',
        'subjects',
        ]
        depth = 1



