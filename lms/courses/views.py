from re import L
import re
from django.db.models import manager
from django.shortcuts import redirect, render
from rest_framework import serializers

from rest_framework.views import APIView

from .models import *
from .serializers import *
from rest_framework.response import Response
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import PackageForm
import json


def add_course(request):
    return render(request ,'course/add_course.html')

def subjects(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        Subject.objects.create(
            subject_title = subject
        )
        messages.success(request, 'Subject created')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    context = {'subjects' : Subject.objects.all()}
    return render(request , 'course/subjects.html' , context)


def subject_chapters(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        chapter_title = request.POST.get('chapter_title')
        subject_obj = Subject.objects.get(uid = subject)
        SubjectChapters.objects.create(
            subject =subject_obj,
            chapter_title=chapter_title
        )
        messages.success(request, 'Subject Chapter created')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    context = {'subjects' : Subject.objects.all(), 'subject_chapters' : SubjectChapters.objects.all()}
    return render(request , 'course/subject_chapters.html' , context)


def lessons(request):
    context = {'lessons' : Lessons.objects.all()}
    return render(request , 'course/lessons.html' , context)


def add_package(request):
    context = {'forms' : PackageForm}

    if request.method == 'POST':
        package_title = request.POST.get('package_title')
        package_obj = CoursePackage.objects.create(
            package_title= package_title
        )
        return redirect(f'/api/courses/add-subjects-package/{package_obj.uid}/')

    return render(request , 'course/add_package.html' , context)


def course_packages(request):
    context = {'course_packages' : CoursePackage.objects.all()}
    return render(request , 'pacakage.html')

def add_subjects_courses(request,uid):
    context = {
    'subjects' : Subject.objects.all(),
    'chapters' : SubjectChapters.objects.all()[0:5],
    'course_package_uid' :uid,
    'subject_uid' :request.GET.get('uid') ,
    }
    if request.GET.get('uid'):
        course_package_obj = CoursePackage.objects.get(uid = uid)
        chapter_obj = SubjectChapters.objects.get(uid = request.GET.get('uid'))

        lessons = chapter_obj.subject_lessons.all()
        
        course_package_subject_obj, _ = CoursePackageSubjects.objects.get_or_create(
            course_package =course_package_obj,
            subject = chapter_obj.subject
        )

        course_package_subject_chapter_obj,_ = CoursePackageChapters.objects.get_or_create(
         course_package_subject = course_package_subject_obj,
            subject_chapter    = chapter_obj
        )
        

        payload = []
        old_lessons = []
        for lesson in course_package_subject_chapter_obj.pacakge_subject_chapters_lessons.all():
            old_lessons.append(lesson.lesson.uid)

        print(old_lessons)

        for lesson in lessons:
            print(lesson.uid)

            if lesson.uid in old_lessons:
                payload.append({
                    'uid' : lesson.uid,
                    'is_free' : lesson.is_free,
                    'lesson_title' : lesson.lesson_title,
                    'is_added' : True,
                    'created_at' : lesson.created_at,
                })

            else:
                payload.append({
                    'uid' : lesson.uid,
                    'is_free' : lesson.is_free,
                    'lesson_title' : lesson.lesson_title,
                    'is_added' : False,
                    'created_at' : lesson.created_at,

                })
            
        context['lessons'] = payload
        context['selected_subject'] = chapter_obj.subject.uid



    #print(context)
    return render(request , 'course/add_subjects_courses.html' , context)



def add_lessons(request):
    context = {'subject_chapters' : SubjectChapters.objects.all()}
    if request.method == 'POST':
        chapters = request.POST.getlist('chapters')
        lesson_title = request.POST.get('lesson_title')
        video_uploaded_on = request.POST.get('video_uploaded_on')
        video_link = request.POST.get('video_link')
        for chapter in chapters:
            Lessons.objects.get_or_create(
                lesson_title =lesson_title,
                video_uploaded_on =video_uploaded_on,
                video_link    =video_link,
                subject_chapters = SubjectChapters.objects.get(uid = chapter)
            )

        messages.success(request, 'Lesson create Successfully')
                
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))





    return render(request , 'course/add_lessons.html' , context)



class CoursesView(APIView):

    def get(self , request):
        course_objs = CoursePackage.objects.all()
        serializer = CourseSerializer(course_objs , many=True)
     
        return Response({'status' : 200 , 'data' :serializer.data})


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
            chapter_obj = SubjectChapters.objects.get(uid = request.GET.get('uid'))
            course_package_obj = CoursePackage.objects.get(uid = request.GET.get('course_package_uid'))
            
            course_package_chapter_obj = CoursePackageChapters.objects.filter(
                course_package_subject__course_package = course_package_obj,
                subject_chapter = chapter_obj
            ).first()

    



            lessons = chapter_obj.subject_lessons.all()
            
            new_serializer = LessonSerializer(lessons , many = True)
            
            payload = []
            if course_package_chapter_obj:
                for data in new_serializer.data:
                    if CoursePackageLessons.objects.filter(
                        course_package_chapter = course_package_chapter_obj,
                        lesson = Lessons.objects.get(uid = data['uid'])
                        ).exists():
                        payload.append({
                        'uid' : data['uid'],
                        'is_added' : True,
                        'lesson_title' : data['lesson_title']
                            })
                       
                    else:
                        payload.append({
                            'uid' : data['uid'],
                            'is_added' : False,
                            'lesson_title' : data['lesson_title']
                        })

            
            print(payload)



           
            return Response({'status' : 200 , 'data' :payload})

        except Exception as e:
            print(e)        
        return Response({'status' : 400 , 'message' : 'Something went wrong'})

from rest_framework.permissions import IsAuthenticated
import sys, os
class SaveCoursePackage(APIView):
    permission_classes = [IsAuthenticated]
    def post(self , request):
        response = {'status' : 400 , 'message' : 'Something went wrong'}
        try:
            data = request.data
            print(data)
            course_package_obj = CoursePackage.objects.get(uid = '8974c82a-a57d-4091-96b1-65db8104d546')
            _subject_uid = data.get('subject_uid')
            _chapter_uid = data.get('chapter_uid')
            _lesson_uid = data.get('lesson_uid')

            
            package_subject , _ = CoursePackageSubjects.objects.get_or_create(
                course_package=course_package_obj,
                subject = Subject.objects.get(uid = _subject_uid)
                )
            
            package_chapter , _  = CoursePackageChapters.objects.get_or_create(
                course_package_subject=package_subject ,
                subject_chapter = SubjectChapters.objects.get(uid= _chapter_uid)
            )
            
            i = 1
            for _lesson in _lesson_uid:
                package_lessons = CoursePackageLessons.objects.get_or_create(
                    course_package_chapter = package_chapter,
                    lesson = Lessons.objects.get(uid=_lesson),
                    sequence = i
                )

            response['status'] = 200  
            response['message'] = 'Subject Added'  

            return Response(response)



        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

        return Response(response)


def live_stream_view(request , id):
    context = {'live' : LiveStream.objects.get(uid = id)}
    return render(request , 'live.html' , context)