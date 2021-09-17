
from django.utils.translation import LANGUAGE_SESSION_KEY
from rest_framework import exceptions, serializers
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


class VideoSerializer(serializers.ModelSerializer):
    video_link = serializers.CharField(required = True)
    class Meta:
        model = Video
        exclude = ['created_at' , 'updated_at']

class DocumentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Document
        exclude = ['created_at' , 'updated_at']
 


class LessonSerializer(serializers.ModelSerializer):
    document = DocumentSerializer(required = False)
    video = VideoSerializer(required = False)
    lesson_type = serializers.CharField(required = True)
    video_platform = serializers.CharField(required = True)
    is_free = serializers.BooleanField(required= True)

    class Meta:
        model = Lessons
        exclude = ['created_at' , 'updated_at']

    def create(self , validated_data):
        try:
            lesson_title = validated_data['lesson_title']
            chapter = validated_data['chapter']
            lesson_type = validated_data['lesson_type']
            video_platform = validated_data['video_platform']
            is_free = validated_data['is_free']
            video_obj = None
            document_obj = None
            if 'document' in validated_data:
                document = validated_data['document']
                if not document is None: 
                    document_obj = Document.objects.create(
                        document = validated_data['document']['document_file']
                    )
            if 'video'  in validated_data:
                video = validated_data['video']
                video_obj = Video.objects.create(
                    #video_uploaded_on = validated_data['video']['video_uploaded_on'],
                    video_link = validated_data['video']['video_link']
                )

            
            obj = Lessons.objects.create(
                lesson_title = lesson_title,
                chapter = chapter,
                lesson_type = lesson_type,
                video_platform = video_platform,
                is_free = is_free,
                video = video_obj,
                document = document_obj
            )


            return obj

        except Exception as e :
            print(e)


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


class CoursePackageSerializer(serializers.ModelSerializer):
    class Meta:
        model= CoursePackage
        fields = ['uid' , 'package_title' ]

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


