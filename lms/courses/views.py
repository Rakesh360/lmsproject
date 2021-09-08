from re import L, sub
import re
from django.db.models import manager
from django.db.models.query import RawQuerySet
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
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q

@staff_member_required(login_url='/accounts/login/')
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

def edit_subject(request ,uid):
    try:
        subject_obj = Subject.objects.get(uid = uid)
        if request.method == 'POST':
            subject_obj.subject_title = request.POST.get('subject')
            subject_obj.save()
            messages.success(request, 'Subject updated')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        context = {'subject' : Subject.objects.get(uid = uid)}
        return render(request , 'course/edit_subject.html' , context)
    except Exception as e:
        print(e)




@staff_member_required(login_url='/accounts/login/')
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

def edit_subject_chapter(request , uid):
    try:
        subject_chapter_obj = SubjectChapters.objects.get(uid = uid)
        if request.method == 'POST':
            subject = request.POST.get('subject')
            chapter_title = request.POST.get('chapter_title')
            subject_obj = Subject.objects.get(uid = subject)
            subject_chapter_obj.subject = subject_obj
            subject_chapter_obj.chapter_title = chapter_title
            subject_chapter_obj.save()
          
            messages.success(request, 'Subject Chapter updated')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        context = {'subjects' : Subject.objects.all(), 'subject_chapter' :  SubjectChapters.objects.get(uid = uid)}
        return render(request , 'course/edit_subject_chapters.html' , context)

    except Exception as e:
        print(e)




@staff_member_required(login_url='/accounts/login/')
def lessons(request):
    context = {'lessons' : Lessons.objects.all()}
    return render(request , 'course/lessons.html' , context)

@staff_member_required(login_url='/accounts/login/')
def add_package(request):
    context = {'forms' : PackageForm}

    if request.method == 'POST':
        package_title = request.POST.get('package_title')
        package_description = request.POST.get('package_description')
        actual_price  = request.POST.get('actual_price') 
        selling_price  = request.POST.get('selling_price')
        sell_from  = request.POST.get('sell_from')
        sell_till  = request.POST.get('sell_till')
        web_image = request.FILES['web_image']
        mobile_image = request.FILES['mobile_image']

        package_obj = CoursePackage.objects.create(
            package_title= package_title,
            package_description = package_description,
            actual_price = actual_price,
            selling_price = selling_price,
            sell_from = sell_from,
            sell_till = sell_till,
            web_image = web_image,
            mobile_image = mobile_image,
        )
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request , 'course/add_package.html' , context)

@staff_member_required(login_url='/accounts/login/')
def course_package_edit(request , uid):
    try:
        if request.method == 'POST':
            package_title = request.POST.get('package_title')
            package_description = request.POST.get('package_description')
            actual_price  = request.POST.get('actual_price') 
            selling_price  = request.POST.get('selling_price')
            sell_from  = request.POST.get('sell_from')
            sell_till  = request.POST.get('sell_till')
            package_obj = CoursePackage.objects.get(uid = uid)
            package_obj.package_title= package_title
            package_obj.package_description = package_description
            package_obj.actual_price = actual_price
            package_obj.selling_price = selling_price
            package_obj.sell_from = sell_from
            package_obj.sell_till = sell_till
            package_obj.save()
            messages.success(request, 'Course Package Updated')

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        context = {'course_package' : CoursePackage.objects.get(uid = uid)}
        

        return render(request , 'course/course-package/course_package_edit.html' , context)
    except Exception as e:
        print(e)
    return redirect('/error/')
@staff_member_required(login_url='/accounts/login/')
def course_packages(request):
    context = {'course_packages' : CoursePackage.objects.all()}
    return render(request , 'course/package.html' , context)


@staff_member_required(login_url='/accounts/login/')
def add_subjects_courses(request,uid):
    context = {
    'subjects' : Subject.objects.all(),
    'course_package_uid' :uid,
    }
    
    course_package_obj = CoursePackage.objects.get(uid = uid)

    if request.GET.get('subject_uid'):
        subject_uid = Subject.objects.get(uid = request.GET.get('subject_uid'))
        chapters = SubjectChapters.objects.filter(subject=subject_uid)
        context['chapters']  = chapters
        context['subject_uid'] = subject_uid
        context['selected_subject'] = subject_uid.uid



    if request.GET.get('uid'):
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


        course_package_add_chapters = []
        for chapter in course_package_subject_obj.pacakge_subject_chapters.all():
            course_package_add_chapters.append(chapter.subject_chapter.uid)

        context['old_lessons'] = old_lessons
        context['lessons'] = lessons
        context['selected_subject'] = chapter_obj.subject.uid
        context['course_package_add_chapters'] = course_package_add_chapters

    course_package_add_subjects = []
    for subject in course_package_obj.pacakge_subjects.all():
        course_package_add_subjects.append(subject.subject.uid)

    context['course_package_add_subjects'] = course_package_add_subjects


    #print(context)
    return render(request , 'course/add_subjects_courses.html' , context)

@staff_member_required(login_url='/accounts/login/')
def course_tree(request,course_package_uid):
    context = {'course_package' : CoursePackage.objects.get(uid = course_package_uid)}
    return render(request , 'course/course_tree.html',context)

@staff_member_required(login_url='/accounts/login/')
def add_lessons(request):
    context = {'subject_chapters' : SubjectChapters.objects.all()}
    if request.method == 'POST':
        chapters = request.POST.get('chapters')
        lesson_title = request.POST.get('lesson_title')
        video_uploaded_on = request.POST.get('video_uploaded_on')
        video_link = request.POST.get('video_link')
        is_free = request.POST.get('is_free')
        lesson_type = request.POST.get('lesson_type')
        
        lesson_obj ,_ = Lessons.objects.get_or_create(
            lesson_title =lesson_title,
            is_free = is_free,
            subject_chapters = SubjectChapters.objects.get(uid = chapters)
        )


        if lesson_type == 'Video':
            obj = Video.objects.create(
               video_uploaded_on =video_uploaded_on,
               video_link    =video_link,
            )
            lesson_obj.video = obj
        elif lesson_type == 'Document':
            obj = Document.objects.create(
                document_file =  request.FILES['document']
            )
            lesson_obj.document = obj
        else:
            obj = Video.objects.create(
               video_uploaded_on =video_uploaded_on,
               video_link    =video_link,
            )
            lesson_obj.video = obj
            obj = Document.objects.create(
                document_file =  request.FILES['document']
            )
            lesson_obj.document = obj

        lesson_obj.save()

        messages.success(request, 'Lesson create Successfully')
                
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request , 'course/add_lessons.html' , context)
@staff_member_required(login_url='/accounts/login/')
def update_lesson(request , uid):
    try:
        lesson_obj = Lessons.objects.get(uid = uid)
        if request.method == 'POST':
            chapters = request.POST.get('chapters')
            lesson_title = request.POST.get('lesson_title')
            video_uploaded_on = request.POST.get('video_uploaded_on')
            video_link = request.POST.get('video_link')
            is_free = request.POST.get('is_free')
            lesson_type = request.POST.get('lesson_type')
    
            lesson_obj.lesson_title =lesson_title
            lesson_obj.is_free = is_free
            lesson_obj.subject_chapters = SubjectChapters.objects.get(uid = chapters)
            lesson_obj.lesson_type = lesson_type
            if lesson_type == 'Video':
                obj = Video.objects.create(
                video_uploaded_on =video_uploaded_on,
                video_link    =video_link,
                )
                lesson_obj.video = obj
            elif lesson_type == 'Document':
                obj = Document.objects.create(
                    document_file =  request.FILES['document']
                )
                lesson_obj.document = obj
            else:
                obj = Video.objects.create(
                video_uploaded_on =video_uploaded_on,
                video_link    =video_link,
                )
                lesson_obj.video = obj
                obj = Document.objects.create(
                    document_file =  request.FILES['document']
                )
                lesson_obj.document = obj

            lesson_obj.save()

            messages.success(request, 'Lesson update Successfully')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except Exception as e:
        print(e)
    
    context = {'lesson' : lesson_obj , 'subject_chapters' : SubjectChapters.objects.all()}
    return render(request , 'course/update_lesson.html',context )


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
                        lesson_dict['sequence'] = lesson.sequence
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


def live_stream_view(request , id):
    context = {'live' : LiveStream.objects.get(uid = id)}
    return render(request , 'live.html' , context)





################ DELETE REQUEST ###########

@staff_member_required(login_url='/accounts/login/')
def delete_subject(request):
    try:
        Subject.objects.get(uid = request.GET.get('uid')).delete()
    except Exception as e:
        print(e)
    messages.success(request, 'Subject Deleted')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
@staff_member_required(login_url='/accounts/login/')
def delete_chapter(request):
    try:
        SubjectChapters.objects.get(uid = request.GET.get('uid')).delete()
    except Exception as e:
        print(e)
    messages.success(request, 'Chapter Deleted')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@staff_member_required(login_url='/accounts/login/')
def delete_lesson(request ):
    try:
        Lessons.objects.get(uid = request.GET.get('uid')).delete()
    
    except Exception as e:
        print(e)
    messages.success(request, 'Lesson Deleted')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
 

@staff_member_required(login_url='/accounts/login/')
def delete_course_package(request ):
    try:
        CoursePackage.objects.get(uid = request.GET.get('uid')).delete()
    
    except Exception as e:
        print(e)
    messages.success(request, 'Course Package Deleted')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
 

def test(request):
    return render(request , 'test/test.html')

def create_test(request):
    return render(request , 'test/create_test.html')
    


def create_live(request):
    context = {
        'course_pacakges' : CoursePackage.objects.all(),
        'subjects' : Subject.objects.all(),
        'chapters' : SubjectChapters.objects.all(),
    }

    if request.method == 'POST':
        image = request.FILES.get('image')
        live_url = request.POST.get('live_url')
        time = request.POST.get('time')
        date = request.POST.get('date')
        chapter = request.POST.get('chapter')
        subject = request.POST.get('subject')
        package = request.POST.get('package')
        live_name = request.POST.get('live_name')

        GoLive.objects.create(
            course_package = package,
            subject = subject,
            chapter = chapter,
            live_name = live_name,
            live_url = live_url,
            image = image,
            live_time = time,
            live_date = date,
        )
        messages.success(request, 'Your Live is created')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
 

    return render(request , 'live/create_live.html', context)
                                                                                                      