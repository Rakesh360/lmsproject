
from functools import partial
from re import sub
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

    def patch(self , request):
        try:
            data = request.data
            if data.get('course_package_uid') is None:
                return Response({
                'status' : False,
                'message' : f'course package uid is required ',
                'data' : {}

            })
        

            obj = CoursePackage.objects.get(uid = data.get('course_package_uid'))

            serializer = CoursePackageSaveSerializer(obj , data = data , partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                'status' : True,
                'message' : f'course package updated',
                'data' : serializer.data
                })
            
            return Response({
                'status' : False,
                'message' : f'course package not updated',
                'data' : serializer.errors

            })
        except Exception as e:
            print(e)
            return Response({
                    'status' : False,
                    'message' : f'{str(e)}',
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
                print(e)
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
                subject_dict['uid'] = subject.uid
                subject_dict['subject_title'] = subject.subject.subject_title
                subject_dict['subject_uid'] = subject.subject.uid
                subject_dict['s_no']  = subject.s_no
                chapters = []
                for chapter in subject.pacakge_subject_chapters.all():
                    chapter_dict = {}
                    chapter_dict['uid'] = chapter.uid
                    chapter_dict['chapter_title'] = chapter.subject_chapter.chapter_title
                    chapter_dict['chapter_uid'] = chapter.subject_chapter.uid
                    chapter_dict['s_no']  = chapter.s_no

                    lessons = []
                    for lesson in chapter.pacakge_subject_chapters_lessons.all():
                        lesson_dict = {}
                        lesson_dict['uid'] = lesson.uid
                        lesson_dict['lesson_title'] = lesson.lesson.lesson_title
                        lesson_dict['lesson_uid'] = lesson.lesson.uid
                        lesson_dict['s_no']  = lesson.s_no

                       

                        lessons.append(lesson_dict)
                    chapter_dict['lessons'] = lessons
                        
                    chapters.append(chapter_dict)
            
                subject_dict['chapters'] = chapters
                subjects.append(subject_dict)
                subject_dict = {}

            course_package_dict['subjects'] = subjects
            course_package_dict['course_package_uid'] = course_obj.uid
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



class RemoveCoursePackageLesson(APIView):
    def post(self , request):
        try:
            data = request.data
            if data.get('lesson_uid') is None and data.get('course_package_uid') is None:
                return Response({
                    'status' : 400,
                    'message' : 'lesson_uid and course_package_uid both are required',
                    'data' : {}
                })
        
            lessob_obj = None
            course_package_obj = None
            try:
                lessob_obj = Lessons.objects.get(uid = data.get('lesson_uid'))
            except Exception as e:
                return Response({
                        'status' : 400,
                        'message' : 'invalid lesson_uid',
                        'data' : {}
                    })
        
            try:
                course_package_obj = CoursePackage.objects.get(uid = data.get('course_package_uid'))
            except Exception as e:
                return Response({
                        'status' : 400,
                        'message' : 'invalid course_package_uid',
                        'data' : {}
                    })
            
            CoursePackageLessons.objects.get(
                course_package_chapter__course_package_subject__course_package = course_package_obj,
                lesson = lessob_obj
            ).delete()

            return Response({
                'satus' : 200,
                'message' : 'Lesson removed'
            })
        
        except Exception as e:
            return Response({
                'status' : 400,
                'message' : 'lesson does not exists in package'
            })




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
                if packages == 'all':
                    i = 0
                    for package in CoursePackage.objects.all():
                        try:
                            course_package_obj = package
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
    
    def patch(self , request):
        try:
            data = request.data
            if data.get('uid') is None:
                return Response({
                    'status' : False,
                    'message' : 'uid is required'
                })
            obj = Lessons.objects.get(uid = data.get('uid'))
            serializer = LessonSerializer( obj,data = request.data , partial=True)

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
                        try:
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
                        except Exception as e:
                            print(e)
                        return Response({
                            'status' : True,
                            'data' : serializer.data,
                            'message' : 'lesson updated'
                        })
                return Response({
                        'status' : True,
                        'data' : serializer.data,
                        'message' : 'lesson updated'
                    })

           

            return Response({
                'status' : False,
                'message' : 'lesson not updated',
                'data' : serializer.errors
            })
        except Exception as e:
            print(e)
            return Response({
                'status' : False,
                'message' : 'lesson not updated',
                'data' : f' error {str(e)}'
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

from rest_framework import status, viewsets
class DocumentUpload(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class CouponView(APIView):
    queryset = Coupoun.objects.all()
    serializer_class = CoupounSerializer

    def list(self , request):
        courpon_code = request.GET.get('coupon_code')
        if courpon_code:
            obj = Coupoun.objects.filter(coupon_code = courpon_code).exists()

            return Response({
                'status' : 200,
                'message' : obj
            })
        return Response({
                'status' : 400,
                'message' : 'coupon_code is required'
            })

    def post(self , request):
        try:
            data = request.data
            if data.get('courses') == 'all':
                objs = CoursePackage.objects.all()
                payload = []
                for obj in objs:
                    payload.append(obj.uid)
                data['courses'] = payload

            print(data)

            serializer = CoupounSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status' : 200,
                    'message' : 'coupon added',
                    'data' : serializer.data
                })
            
            return Response({
                    'status' : 400,
                    'message' : 'coupon not added',
                    'data' : serializer.errors
                })
        except Exception as e:
            return Response({
                    'status' : 400,
                    'message' : 'something went wrong',
                    'data' :  {}
                })

    def patch(self , request):
        try:
            data = request.data
            if data.get('courses') == 'all':
                objs = CoursePackage.objects.all()
                payload = []
                for obj in objs:
                    payload.append(obj.uid)
                data['courses'] = payload
            obj = Coupoun.objects.get(uid = data.get('uid'))
            serializer = CoupounSerializer(obj ,data = data , partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status' : 200,
                    'message' : 'coupon updated',
                    'data' : serializer.data
                })
        
            return Response({
                    'status' : 400,
                    'message' : 'coupon not added',
                    'data' : serializer.errors
                })
        except Exception as e:
            return Response({
                    'status' : 400,
                    'message' : 'something went wrong',
                    'data' :  {}
                })




class SliderView(viewsets.ModelViewSet):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer



    def patch(self , request):
        try:
            data =  request.data
            
            if data.get('uid') is None:
                return Response({'status' : 400 , 'message' : 'uid is required'})
            try:
                obj = Coupoun.objects.get(uid = data.get('uid'))
            except Exception as e:
                return Response({'status' : 400 , 'message' : ' invalid uid'})
            
            serializer = CoupounSerializer(obj , data = data ,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status' : 200 , 'message' : 'coupon updated' , 'data' : serializer.data})

            return Response({'status' : 200 , 'message' : 'error' , 'data' : serializer.errors})
        
        except Exception as e:
            print(e)
            return Response({'status' : 400 , 'message' : ' something went wrong'})

    
    def delete(self , request):
        try:
            data =  request.data
            
            if data.get('uid') is None:
                return Response({'status' : 400 , 'message' : 'uid is required'})
            try:
                obj = Coupoun.objects.get(uid = data.get('uid')).delete()
            except Exception as e:
                return Response({'status' : 400 , 'message' : ' invalid uid'})
            return Response({'status' : 200 , 'message' : 'deleted' })
        
        except Exception as e:
            print(e)
            return Response({'status' : 400 , 'message' : ' something went wrong'})

    
                
            




 





class CoursePackageSerial(APIView):
    def post(self , request):
        try:
            data = request.data
            course_package_obj = CoursePackage.objects.get(uid = data.get('coure_package_uid'))
            sequence_for = data.get('sequence_for')

            if sequence_for == 'subject':
                if data.get('subjects'):
                    for subject in data.get('subjects'):
                        subject_uid = (subject['subject_uid'])
                        package_subject_obj , _ = CoursePackageSubjects.objects.get_or_create(
                            course_package = course_package_obj,
                            subject = Subject.objects.get(uid = subject['subject_uid'])
                        )
                        package_subject_obj.s_no = subject['s_no']
                        package_subject_obj.save()

            elif sequence_for == 'chapter':
                if data.get('chapters'):
                    for chapter in data.get('chapters'):
                        package_chapter_obj ,_ = CoursePackageChapters.objects.get_or_create(
                        course_package_subject = CoursePackageSubjects.objects.get(uid = chapter['uid']),
                        subject_chapter = SubjectChapters.objects.get(uid = chapter['subject_uid'])
                        )
                        package_chapter_obj.s_no = chapter['s_no']
                        package_chapter_obj.save()
                        
            elif sequence_for == 'lesson':
                if data.get('lessons'):
                    for lesson in data.get('lessons'):
                        package_lesson_obj , _ = CoursePackageLessons.objects.get_or_create(
                            course_package_chapter =CoursePackageChapters.objects.get(uid = lesson['uid']) ,
                            lesson = Lessons.objects.get(uid = lesson['lesson_uid']),
                            
                        )
                        package_lesson_obj.s_no = lesson['s_no']
                        package_lesson_obj.save()

        
            return Response({
                'status' : True,
                'message' : 'sequence updated',
                'data' : {}
            })

               

        except Exception as e:
            import sys, os
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

            print(e)
            return Response({
                'status' : False,
                'message' : f'something went wrong error {str(e)}',
                'data' : {}
            })
