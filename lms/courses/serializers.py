
from django.db.models import fields
from django.utils.translation import LANGUAGE_SESSION_KEY
from rest_framework import exceptions, serializers
from base_rest.utils import *
from dashboard.models import NotificationLogs
from .models import *
from pytube import YouTube


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

    video = VideoSerializer(required = False)
    lesson_type = serializers.CharField(required = True)
    video_platform = serializers.CharField(required = False)
    is_free = serializers.BooleanField(required= True)

    class Meta:
        model = Lessons
        exclude = ['created_at' , 'updated_at']

    def create(self , validated_data):
        try:
            print(validated_data)
            lesson_title = validated_data['lesson_title']
            chapter = validated_data['chapter']
            lesson_type = validated_data['lesson_type']
            is_free = validated_data['is_free']
            video_obj = None
            document_obj = None
            video_platform = None
            if 'document' in validated_data:
                document_obj = validated_data['document']
                # if not document is None: 
                #     document_obj = Document.objects.get(
                #         uid = validated_data['document']
                #     )
                #     print(document_obj)
            if 'video'  in validated_data:
                video = validated_data['video']
                download_link = None
                try:
                    yt = YouTube(f"http://youtube.com/watch?v={validated_data['video']['video_link']}")
                    yt.streams.all()  
                    download_link = yt.streams[1].url
                except Exception as e:
                    print(e)
                    
                video_obj = Video.objects.create(
                    video_link = validated_data['video']['video_link'],
                    download_link = download_link
                )
            
            if 'video_platform' in validated_data:
                video_platform = validated_data['video_platform']
            else:
                video_platform = 'Youtube'

            
            obj = Lessons.objects.create(
                lesson_title = lesson_title,
                chapter = chapter,
                lesson_type = lesson_type,
                is_free = is_free,
                video_platform = video_platform,
                video = video_obj,
                document = document_obj
            )


            return obj

        except Exception as e :
            print(e)

    
    def update(self , instance , validated_data):
        instance.lesson_title = validated_data.get('lesson_title' , instance.lesson_title)
        instance.chapter = validated_data.get('chapter' , instance.chapter)
        instance.lesson_type = validated_data.get('lesson_type' , instance.lesson_type)
        instance.video_platform = validated_data.get('video_platform' , instance.video_platform)
        instance.is_free = validated_data.get('is_free' , instance.is_free)
        video_obj = None
        document_obj = None
        if 'document' in validated_data:
            document_obj = validated_data['document']
            # if not document is None: 
            #     document_obj = Document.objects.get(
            #         uid = validated_data['document']
            #     )
            #     print(document_obj)
        if 'video'  in validated_data:
            video = validated_data['video']
            video_obj = Video.objects.create(
                #video_uploaded_on = validated_data['video']['video_uploaded_on'],
                video_link = validated_data['video']['video_link']
            )


        instance.video = video_obj
        instance.document = document_obj


        instance.save()
        return instance




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

class CoursePackageSaveSerializer(serializers.ModelSerializer):
    package_type = serializers.CharField(required = True)
    
    class Meta:
        model = CoursePackage
        exclude = ['updated_at']

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



class GoLiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoLive
        exclude = ['created_at' , 'updated_at']    

class NotificationLogsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NotificationLogs
        exclude = [ 'updated_at']    

class CoursePackageUid(serializers.ModelSerializer):
    class Meta:
        model = CoursePackage
        fields = ['uid' , ]

class CoupounSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupoun
        exclude = ['created_at' , 'updated_at']

class CoupounOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupoun
        fields = ['coupon_code' ,]



class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        exclude = ['created_at' , 'updated_at']
