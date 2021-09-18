
from django.db.models import manager
from django.db.models.query import RawQuerySet
from django.shortcuts import redirect, render
from rest_framework import exceptions, serializers
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from .forms import PackageForm
import json
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q


class CoursesView(APIView):

    def get(self , request):
        limit = 'no_limit'
        if request.GET.get('limit'):
            limit = request.GET.get('limit')

        if limit == 'no_limit':
            course_objs = CoursePackage.objects.all()
        else:
            try:
                limit = int(limit)
            except Exception as e:
                print(e)
                return Response({'status' : 400 , 'data' :{} , 'message' : 'not a valid integer'})

            course_objs = CoursePackage.objects.all()[0:limit]

        payload = []



        for course_obj in course_objs:
            course_package_dict = {}
            course_package_dict['uid'] = course_obj.uid
            course_package_dict['package_title'] = course_obj.package_title

            course_package_dict['package_description'] = course_obj.package_description
            course_package_dict['actual_price'] = course_obj.actual_price
            course_package_dict['selling_price'] = course_obj.selling_price
            course_package_dict['sell_from'] = course_obj.selling_price
            course_package_dict['sell_till'] = course_obj.selling_price
            course_package_dict['web_image'] = '/media/' + str(course_obj.web_image)
            course_package_dict['mobile_image'] ='/media/' + str(course_obj.mobile_image)

            subjects = [] 
            for subject in course_obj.pacakge_subjects.all():
                subject_dict = {}
                subject_dict['subject_title'] = subject.subject.subject_title
                chapters = []
                for chapter in subject.pacakge_subject_chapters.all():
                    chapter_dict = {}
                    chapter_dict['chapter_title'] = chapter.subject_chapter.chapter_title
                    lessons = []
                    for lesson in chapter.pacakge_subject_chapters_lessons.all():
                        lesson_dict = {}
                        lesson_dict['sequence'] = lesson.s_no
                        lesson_dict['lesson_title'] = lesson.lesson.lesson_title
                        lesson_dict['lesson_type'] = lesson.lesson.lesson_type
                        lesson_dict['is_free'] = lesson.lesson.is_free
                        lesson_dict['created_at'] = lesson.created_at
                        lesson_dict['video_link'] = ''
                        lesson_dict['video_uploaded_on'] = ''
                        lesson_dict['document_file'] = ''
                        try:
                            if lesson.lesson.lesson_type == 'Video':
                                lesson_dict['video_link'] = lesson.lesson.video.video_link
                                lesson_dict['video_uploaded_on'] = lesson.lesson.video.video_uploaded_on
                            elif lesson.lesson.lesson_type == 'Document':
                                lesson_dict['document_file'] = '/media/' +str(lesson.lesson.document.document_file)
                            elif lesson.lesson.lesson_type == 'Video + Document':
                                lesson_dict['document_file'] = '/media/' +str(lesson.lesson.document.document_file)
                                lesson_dict['video_link'] = lesson.lesson.video.video_link
                                lesson_dict['video_uploaded_on'] = lesson.lesson.video.video_uploaded_on
                      

                        except Exception as e:
                            print(e)

                        lessons.append(lesson_dict)
                    chapter_dict['lessons'] = lessons
                        
                    chapters.append(chapter_dict)
            
                subject_dict['chapters'] = chapters
                subjects.append(subject_dict)
                subject_dict = {}

            course_package_dict['subjects'] = subjects
            payload.append(course_package_dict)


        return Response({'status' : 200 , 'data' :payload})


class CoursePackageAPI(APIView):
    def get(self , request):
        course_package_objs = CoursePackage.objects.filter(is_active = True)
        serializer = CoursePackageSerializer(course_package_objs , many= True)
        return Response({
            'status' : True ,
            'message' : 'course packages',
            'data' : serializer.data
        })

    def post(self , request):
        try:
            data = request.data
            serializer = CoursePackageSaveSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                'status' : True,
                'message' : f'course package created',
                'data' : serializer.data
                })
            
            return Response({
                'status' : False,
                'message' : f'course package not created',
                'data' : serializer.errors

            })

        
        except Exception as e:
            print(e)
            return Response({
                'status' : False,
                'message' : f'something went wrong {str(e)}',
                'data' : {}
            })

class CoursePackageSubjectsAPI(APIView):
    def get(self , request):
        try:
            uid = request.GET.get('uid')
            if not uid:
                return Response({
                    'status' : False,
                    'message' : 'uid is required',
                    'data' : {}
                })

            try:
                course_obj = CoursePackage.objects.get(uid = uid)
            except Exception as e:
                return Response({
                    'status' : False,
                    'message' : 'invalid uid',
                    'data' : {}
                })

            course_package_dict = {}
            payload = []
            subjects = [] 
            for subject in course_obj.pacakge_subjects.all():
                subject_dict = {}
                subject_dict['subject_title'] = subject.subject.subject_title
                subject_dict['subject_uid'] = subject.subject.uid
                chapters = []
                for chapter in subject.pacakge_subject_chapters.all():
                    chapter_dict = {}
                    chapter_dict['chapter_title'] = chapter.subject_chapter.chapter_title
                    chapter_dict['chapter_uid'] = chapter.subject_chapter.uid
                    lessons = []
                    for lesson in chapter.pacakge_subject_chapters_lessons.all():
                        lesson_dict = {}
                        lesson_dict['lesson_title'] = lesson.lesson.lesson_title
                        lesson_dict['uid'] = lesson.lesson.uid
                       

                        lessons.append(lesson_dict)
                    chapter_dict['lessons'] = lessons
                        
                    chapters.append(chapter_dict)
            
                subject_dict['chapters'] = chapters
                subjects.append(subject_dict)
                subject_dict = {}

            course_package_dict['subjects'] = subjects
            payload.append(course_package_dict)

            return Response({
                'status' : True,
                'message' : 'fetch course package info',
                'data' : course_package_dict
            })



        
        except Exception as e:
            return Response({
                    'status' : False,
                    'message' : 'invalid uid',
                    'data' : {}
                })




class SubjectsView(APIView):
    def get(self , request):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects , many   = True)
        return Response({
            'status' : True,
            'message' : 'all subjects',
            'data' : serializer.data
        })

class ChaptersView(APIView):
    
    def get(self , request):
        try:
            subject_uid = Subject.objects.get(uid = request.GET.get('uid'))
            chapters = SubjectChapters.objects.filter(subject=subject_uid)
            serializer = SubjectChaptersSerializer(chapters , many=True)

            return Response({'status' : 200 , 'data' :serializer.data})

        except Exception as e:
            print(e)        
        return Response({'status' : 400 , 'message' : 'Something went wrong'})





class LessonsView(APIView):
    def get(self , request):
        try:
            if request.GET.get('uid') is None:
                return Response({
                    'status' : False,
                    'message' : 'uid is required'
                })
            chapter_obj = SubjectChapters.objects.get(uid = request.GET.get('uid'))
            
            lessons = chapter_obj.subject_lessons.all()
            serializer = LessonSerializer(lessons , many = True)        
            return Response({'status' : 200 , 'data' :serializer.data})

        except Exception as e:
            print(e)        
        return Response({'status' : 400 , 'message' : 'Something went wrong invalid uid'})

    def post(self , request):
        try:
            data = request.data
            serializer = LessonSerializer(data = request.data)

            if serializer.is_valid():
                serializer.save()
                lesson_obj = Lessons.objects.get(uid = serializer.data['uid'])
                chapter_obj = lesson_obj.chapter
                subject_obj = lesson_obj.chapter.subject
                packages = data.get('packages')
                print(packages)
                if packages:
                    i = 0
                    for package in packages:
                        try:
                            course_package_obj = CoursePackage.objects.get(uid = package['uid'])
                        except Exception as e:
                            return Response({
                                'status' : False,
                                'message' : f'lesson created but not added to packages invalid uid at index {i}'
                            })
                        i = i + 1
                        course_package_subject_obj, _ = CoursePackageSubjects.objects.get_or_create(
                            course_package = course_package_obj,
                            subject = subject_obj
                        )
                        course_package_chapter_obj, _ = CoursePackageChapters.objects.get_or_create(
                            course_package_subject = course_package_subject_obj,
                            subject_chapter = chapter_obj
                        )
                        created_at = package['created_at']

                        CoursePackageLessons.objects.get_or_create(
                            course_package_chapter = course_package_chapter_obj,
                            lesson = lesson_obj,
                            added_at = created_at
                        )

                return Response({
                    'status' : True,
                    'data' : serializer.data,
                    'message' : 'lesson created'
                })
            
            return Response({
                'status' : False,
                'data' : serializer.errors,
                'message' : 'lesson not created'
            })
        
        except Exception as e:
            print(e)
        
        return Response({
                'status' : False,
                'data' : {},
                'message' : 'something went wrong'
            })
         

from rest_framework.permissions import IsAuthenticated
import sys, os
class SaveCoursePackage(APIView):
    permission_classes = [IsAuthenticated]
    def post(self , request):
        response = {'status' : 400 , 'message' : 'Something went wrong'}
        try:
            data = request.data

            course_package_obj = CoursePackage.objects.get(uid = data.get('course_package_uid'))
            _subject_uid = data.get('subject_uid')
            _chapter_uid = data.get('chapter_uid')
            _selected_lesson_uid = data.get('selected_lesson_uid')
            _unselected_lesson_uid = data.get('unselected_lesson_uid')
            

            
            package_subject , _ = CoursePackageSubjects.objects.get_or_create(
                course_package=course_package_obj,
                subject = Subject.objects.get(uid = _subject_uid)
                )
            
            package_chapter , _  = CoursePackageChapters.objects.get_or_create(
                course_package_subject=package_subject ,
                subject_chapter = SubjectChapters.objects.get(uid= _chapter_uid)
            )
            
            i = 1
            for _lesson in _selected_lesson_uid:
                print('created')
                package_lessons ,_= CoursePackageLessons.objects.get_or_create(
                    course_package_chapter = package_chapter,
                    lesson = Lessons.objects.get(uid=_lesson),
                    sequence = i
                )
                print(package_lessons)
                i += 1

            for _lesson in _unselected_lesson_uid:
                try:
                    package_lessons = CoursePackageLessons.objects.get(
                        course_package_chapter = package_chapter,
                        lesson = Lessons.objects.get(uid=_lesson)
                    ).delete()
                except Exception as e:
                    print(e)


            response['status'] = 200  
            response['message'] = 'Subject Added'  

            return Response(response)



        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

        return Response(response)


class GoLiveView(APIView):
    def post(self , request):
        try:
            data = request.data
            serializer = GoLiveSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status' : True,
                    'message' : 'Live created Successfully',
                    'data' : serializer.data
                })

            return Response({
                'status' : False,
                    'message' : 'live not created',
                    'data' : serializer.errors
                })  
        except Exception as e:
            print(e)
            return Response({
                'status' : False,
                    'message' : 'something went wrong',
                    'data' : str(e)

                }) 