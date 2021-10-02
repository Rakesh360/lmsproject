from django.http.response import JsonResponse
from orders.models import Order
from django.shortcuts import redirect, render
from accounts.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib import messages
from django.http import HttpResponseRedirect
from .helpers import *
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required(login_url='/accounts/login/')
def dashboard(request):
    return render(request , 'dashboard/dashboard.html')

def send_noti(request):
    send_notify_by_order("A new course has been added" , 'BA arts has been updated check the lastest videos.')
    return JsonResponse({'status' : 200})

def students(request):
    student_objs = Student.objects.all()
    subjects = Subject.objects.all()
    
    if request.GET.get('subject'):
        selected_subjects = request.GET.getlist('subject')
        print(selected_subjects)
        student_objs = student_objs.filter(course__in = selected_subjects)

    if request.GET.get('name'):
        student_objs = student_objs.filter(student_name = request.GET.get('name'))



    page = request.GET.get('page', 1)
    paginator = Paginator(student_objs, 50)
    try:
        student_objs = paginator.page(page)
    except PageNotAnInteger:
        student_objs = paginator.page(1)
    except EmptyPage:
        student_objs = paginator.page(paginator.num_pages)

    return render(request , 'new_dashboard/user/allStudents.html', {'subjects' : subjects, 'student_objs': student_objs })


def send_notification(request):
    context = {'course_packages' : CoursePackage.objects.all()}
    if request.method == 'POST':
        course_packages = request.POST.getlist('course_packages')
        notification_title = request.POST.get('notification_title')
        notification_content = request.POST.get('notification_content')
        order_objs = Order.objects.filter(course__uid__in = course_packages , is_paid = True)

        for order_obj in order_objs:
            student_fcm = order_obj.student.fcm_token

        send_notify_by_order(order_obj,notification_title ,notification_content  )
        messages.success(request, 'Notification Sent')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
         

        

    return render(request , 'students/send_notification.html' , context)


def export_student_list(request):
    return 