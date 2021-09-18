
from django.shortcuts import redirect, render
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

    course_package_add_subjects = []
    for subject in course_package_obj.pacakge_subjects.all():
        course_package_add_subjects.append(subject.subject.uid)

    context['course_package_add_subjects'] = course_package_add_subjects


    #print(context)
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
    return render(request , 'new_dashboard/update_lesson.html',context )




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
    return render(request , 'live/create_live.html', context)



def all_coupons(request ):
    context = {
        'allcoupons' : Coupoun.objects.all(),
        'subjects' : Subject.objects.all(),
        'chapters' : SubjectChapters.objects.all(),
    }
    return render(request , 'new_dashboard/coupons/all_coupons.html' , context)


def add_coupons(request):

    return render(request, 'new_dashboard/coupons/add_coupons.html' , )
            
                                                                                                    