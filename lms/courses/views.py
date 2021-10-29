from django.shortcuts import redirect, render
from rest_framework.permissions import OR

from dashboard.models import NotificationLogs
from orders.models import Order
from .models import *
from .serializers import *
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from .forms import PackageForm
import json
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required(login_url='/accounts/login/')
def add_course(request):
    return render(request ,'course/add_course.html')


def subjects(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        if Subject.objects.filter(subject_title = subject).exists():
            messages.error(request, 'Subject already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        Subject.objects.create(
            subject_title = subject
        )
        messages.success(request, 'Subject created')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    context = {'subjects' : Subject.objects.all()}
    return render(request , 'new_dashboard/all_subjects.html' , context)



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

        if SubjectChapters.objects.filter(
            subject =subject_obj,
            chapter_title=chapter_title
        ).exists():
            messages.error(request, 'Subject Chapter already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    


        SubjectChapters.objects.create(
            subject =subject_obj,
            chapter_title=chapter_title
        )
        messages.success(request, 'Subject Chapter created')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    context = {'subjects' : Subject.objects.all(), 'subject_chapters' : SubjectChapters.objects.all()}
    return render(request , 'new_dashboard/all_topics.html' , context)

def edit_subject_chapter(request , uid):
    try:
        subject_chapter_obj = SubjectChapters.objects.get(uid = uid)
        if request.method == 'POST':
            subject = request.POST.get('subject')
            chapter_title = request.POST.get('chapter_title')
            subject_obj = Subject.objects.get(uid = subject)
            if SubjectChapters.objects.filter(subject =subject_obj,chapter_title=chapter_title).exists():
                messages.error(request, 'Subject Chapter already exists')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

            subject_chapter_obj.subject = subject_obj
            subject_chapter_obj.chapter_title = chapter_title
            subject_chapter_obj.save()
          
            context = messages.success(request, 'Subject Chapter updated')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        
        context = {'subjects' : Subject.objects.all(), 'subject_chapter' :  SubjectChapters.objects.get(uid = uid)}
        return render(request , 'course/edit_subject_chapters.html' , context)
        # return {'status': 'OKOK'}

    except Exception as e:
        print(e)




@staff_member_required(login_url='/accounts/login/')
def lessons(request):
    context = {'lessons' : Lessons.objects.all()}
    return render(request , 'new_dashboard/all_videos.html' , context)

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

    return render(request , 'new_dashboard/add_package.html' , context)

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
    return render(request , 'new_dashboard/all_packages.html' , context)


def package_end_purchase(request , uid):
    try:
        obj = CoursePackage.objects.get(uid = uid)
        obj.end_purchase = not obj.end_purchase
        obj.save()
        messages.success(request, 'Purchase Updated')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    
    except Exception as e:
        return redirect('/')


@staff_member_required(login_url='/accounts/login/')
def add_subjects_courses(request,uid):
    course_package_obj = CoursePackage.objects.get(uid = uid)
    context = {
    'course_package_obj' : course_package_obj,
    'subjects' : Subject.objects.all(),
    'course_package_uid' :uid,
    }
    

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

    # course_package_add_subjects = []
    # for subject in course_package_obj.pacakge_subjects.all():
    #     course_package_add_subjects.append(subject.subject.uid)

    # context['course_package_add_subjects'] = course_package_add_subjects

    # print(context)

    return render(request , 'new_dashboard/edit_subjects_courses.html' , context)

@staff_member_required(login_url='/accounts/login/')
def course_tree(request,course_package_uid):
    context = {'course_package' : CoursePackage.objects.get(uid = course_package_uid)}
    return render(request , 'course/course_tree.html',context)

@staff_member_required(login_url='/accounts/login/')
def add_lessons(request):
    context = {'subject_chapters' : SubjectChapters.objects.all(), 'course_packages' : CoursePackage.objects.all()}

    return render(request , 'new_dashboard/add_lessons.html' , context)

@staff_member_required(login_url='/accounts/login/')
def update_lesson(request , uid):
    try:
        lesson_obj = Lessons.objects.get(uid = uid)
        course_package_lessons = CoursePackageLessons.objects.filter(lesson = lesson_obj)
        #print(course_package_lesson)

        context = {
            'lesson' : lesson_obj ,
            'subject_chapters' : SubjectChapters.objects.all(),
            'course_packages': CoursePackageLessons.objects.all(),
            'all_course_packages' : CoursePackage.objects.all(),
            "course_package_lessons" : course_package_lessons
            }
        return render(request , 'new_dashboard/update_lesson.html',context )

    except Exception as e:
        print(e)
        #return redirect('/')


def go_live(request):
    objs = GoLive.objects.all()
    context = {'objs' : objs}
    return render(request , 'new_dashboard/go_live.html' , context)


@staff_member_required(login_url='/accounts/login/')
def add_live(request):
    context = {'subject_chapters' : SubjectChapters.objects.all(), 'course_packages' : CoursePackage.objects.all()}

    return render(request , 'new_dashboard/add_live.html' , context)

def edit_live(request, uid):
    try:
        obj = GoLive.objects.get(uid = uid)
        context = {
            'live' : obj,
            'subject_chapters' : SubjectChapters.objects.all(),
            'all_course_packages' : CoursePackage.objects.all(),
        }
        return render(request , 'new_dashboard/edit_live.html' , context)
    except Exception as e:
        print(e)
        return redirect('/')

from dashboard.helpers import *

def change_live_status(request , uid):
    try:
        obj = GoLive.objects.get(uid = uid)
        if request.GET.get('status') == 'start':
            obj.is_live_started = True
            obj.save()
            
           
            objs = Order.objects.filter(course__in = obj.courses.all())
            registration_ids = set()
            for o in objs:
                try:
                    registration_ids.add(
                        o.student.fcm_token
                    )
                except Exception as e:
                    print(e)
            registration_ids = list(registration_ids)
            send_notification_packages(registration_ids , f'{obj.live_name} has been started.'  , 'Live has been started please join.')



        elif request.GET.get('status') == 'end':
            obj.is_live_ended = True
            obj.save()
            lesson_obj = Lessons.objects.create(
                lesson_title = obj.live_name ,
                chapter = obj.chapter,
                lesson_type ='Video',
                video = Video.objects.create(
                    video_uploaded_on = 'Youtube',
                    video_link = obj.live_url
                )
            )
            for course_package in obj.courses.all():
                package_subject_obj , _ = CoursePackageSubjects.objects.get_or_create(
                        course_package = course_package,
                        subject = obj.subject
                )
                package_chapter_obj , _ = CoursePackageChapters.objects.get_or_create(
                    course_package_subject = package_subject_obj,
                    subject_chapter = obj.chapter
                )
                package_lesson_obj = CoursePackageLessons.objects.get_or_create(
                    course_package_chapter = package_chapter_obj,
                    lesson = lesson_obj,
                )

            objs = Order.objects.filter(course__in = obj.courses.all())
            registration_ids = set()
            for o in objs:
                try:
                    registration_ids.add(
                        o.student.fcm_token
                    )
                except Exception as e:
                    print(e)
            registration_ids = list(registration_ids)
            send_notification_packages(registration_ids , f'{obj.live_name} has been ended.'  , 'Live has been ended! Video has been added to lesson.')
            obj.delete()
            

        elif request.GET.get('status') == 'cancel':
            print('cancel')
            objs = Order.objects.filter(course__in = obj.courses.all())
            registration_ids = set()
            for o in objs:
                try:
                    registration_ids.add(
                        o.student.fcm_token
                    )
                except Exception as e:
                    print(e)
            registration_ids = list(registration_ids)
            
            send_notification_packages(registration_ids , f'{obj.live_name} has been canceled.'  , 'Live has been cancel. Due to some reason')
            obj.delete()

        #send_notification_packages
        
        messages.success(request, 'Live updated')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


    except Exception as e:
        print(e)
        return redirect('/')

def live_stream_view(request , id):
    context = {'live' : LiveStream.objects.get(uid = id)}
    return render(request , 'live.html' , context)





################ DELETE REQUEST ###########

def delete_package_lesson(request ):
    
    if request.GET.get('lesson_uid') is None and request.GET.get('course_package_uid') is None:
        print("AAAAAAA")
        messages.success(request, 'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


    lessob_obj = None
    course_package_obj = None
    print( request.GET.get('lesson_uid') )
    print(request.GET.get('course_package_uid'))
    try:
        lessob_obj = Lessons.objects.get(uid = request.GET.get('lesson_uid'))
    except Exception as e:
        print(e)
        messages.success(request, 'Something went wrong')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


    try:
        course_package_obj = CoursePackage.objects.get(uid = request.GET.get('course_package_uid'))
    except Exception as e:
        print(e)
        messages.success(request, 'Something went wrong')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    
    CoursePackageLessons.objects.get(
        course_package_chapter__course_package_subject__course_package = course_package_obj,
        lesson = lessob_obj
    ).delete()
    messages.success(request, 'Lesson removed')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



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
    return render(request , 'live/create_live.html', context)

def preview_video(request, uid):
    lesson_obj = Lessons.objects.get(uid = uid)
    live_obj = GoLive.objects.get(uid = uid)
    context = {
        'lesson' : lesson_obj,
        'live' : live_obj,
    }
    
    return render(request , 'new_dashboard/preview_video.html', context)


def preview_video_live(request, uid):
    lesson_obj = GoLive.objects.get(uid = uid)
    context = {
        'lesson' : lesson_obj,
    }
    
    return render(request , 'new_dashboard/preview_video_live.html', context)


def all_coupons(request ):
    context = {
        'allcoupons' : Coupoun.objects.all(),
        'subjects' : Subject.objects.all(),
        'chapters' : SubjectChapters.objects.all(),
    }
    return render(request , 'new_dashboard/coupons/all_coupons.html' , context)


def add_coupons(request):
    context = {
        'course_packages' : CoursePackage.objects.all(),
    }

    return render(request, 'new_dashboard/coupons/add_coupons.html' , context)


def edit_coupon(request, uid):
    context = {
        'course_packages' : CoursePackage.objects.all(),
    'coupon' : Coupoun.objects.get(uid = uid)
    }

    return render(request, 'new_dashboard/coupons/edit_coupon.html' , context)

def remove_coupon(request):
    try:
        course_uid = CoursePackage.objects.get(uid = request.GET.get('course_uid'))
        coupon = Coupoun.objects.get(uid = request.GET.get('coupon'))

        coupon.courses.remove(course_uid)
        messages.success(request, 'Coupon removed')


    except Exception as e:
        print(e)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_coupon(request):
    context = {
        'allcoupons' : Coupoun.objects.all(),
        'subjects' : Subject.objects.all(),
        'chapters' : SubjectChapters.objects.all(),
    }
    try:
        Coupoun.objects.get(uid = request.GET.get('uid')).delete()
    except Exception as e:
        print(e)
    messages.success(request, 'Subject Deleted')
    return render(request, 'new_dashboard/coupons/all_coupons.html' , context)


def all_test(request):
    
    return render(request , 'new_dashboard/tests/all_test.html' )

def add_test(request):
    return render(request , 'new_dashboard/tests/add_test.html' )


def edit_test(request):
    return render(request , 'new_dashboard/coupons/edit_coupons_detail.html')


def all_question(request):
    return render(request , 'new_dashboard/questions/all_questions.html')

def add_question(request):
    return render(request , 'new_dashboard/coupons/add_coupons_question.html')



def send_notification(request):
    context = {
        'course_packages' : CoursePackage.objects.all(),
    }
    if request.method == 'POST':
        notfication_title = request.POST.get('title')
        notification_content = request.POST.get('description')
        notification_image = request.FILES.get('image')
        courses_items = request.POST.getlist('packages')
        obj = NotificationLogs.objects.create(
        notfication_title = notfication_title,
        notification_content = notification_content,
        notification_image = notification_image,
        )
        registration_ids = set()
        print('(((((((((((((((((')
        print(courses_items)
        print('(((((((((((((((((')

        for c in courses_items:
            print(c)
            c_obj = CoursePackage.objects.get(uid = c)
            obj.courses.add(c_obj)
            order_objs = Order.objects.filter(course = c_obj , is_paid = True)
            for order_obj in order_objs:
                registration_ids.add(order_obj.student.fcm_token)

        registration_ids = list(registration_ids)
        if notification_image:
            send_notification_packages(
                registration_ids,
                notfication_title,
                notification_content,
                'http://13.232.227.45/'+str(obj.notification_image))
        else:
             send_notification_packages(
                registration_ids,
                notfication_title,
                notification_content)

        
        
        messages.success(request, 'Notification created')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
 

    return render(request , 'new_dashboard/manage_app/send_notification.html', context)


def all_slider(request):
    if request.method=="POST":
        image = request.POST.get('image')
        Slider.objects.create(
            slider_image =image,
            
        )
        messages.success(request, 'Slider created')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    context = {'sliders' : Slider.objects.all()}
    return render(request , 'new_dashboard/manage_app/all_slider.html', context)


@staff_member_required(login_url='/accounts/login/')
def delete_slider(request):
    try:
        Slider.objects.get(uid = request.GET.get('uid')).delete()
    except Exception as e:
        print(e)
    messages.success(request, 'Slider Deleted')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def chat_live(request , room_id):
    obj = GoLive.objects.get(uid = room_id)
    print('@@@@@@@@@@@@@@')
    print(obj.live_url)
    print('@@@@@@@@@@@@@@')

    return render(request , 'new_dashboard/chat_live.html' , context = {
        'room_id' : obj.live_url
    })