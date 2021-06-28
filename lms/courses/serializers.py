
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
        model = CourseChapters
        exclude = ['created_at', 'updated_at']


class CourseSerializer(serializers.ModelSerializer):
    course_category = CourseCategorySerializer()
    course_chapters  = CourseChaptersSerializers(source ="course" , many=True)
    class Meta:
        model = Course
    
        fields = [
        'uid',
        'course_slug',
        'enrolled_students',
        'course_price',
        'course_image',
        'course_upload_on',
        'discount_price',
        'course_description',
        'course_level',
        'course_chapters',
        'course_category'
        ]
        depth = 1



