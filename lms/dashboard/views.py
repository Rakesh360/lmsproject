import re
from django.http.response import JsonResponse
from orders.models import Order
from django.shortcuts import redirect, render
from accounts.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib import messages
from django.http import HttpResponseRedirect
from .helpers import *
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
import uuid
import pandas as pd
from django.conf import settings
@staff_member_required(login_url='/accounts/login/')
def dashboard(request):
    return render(request , 'dashboard/dashboard.html')

def send_noti(request):
    send_notify_by_order("A new course has been added" , 'BA arts has been updated check the lastest videos.')
    return JsonResponse({'status' : 200})

def students(request):
    student_objs = Student.objects.all()
    student_uids = []
    values_for_search = {'search' : '' , 'enroll' : 'all'}
    if request.GET.get('search'):
        search = request.GET.get('search')
        student_objs = Student.objects.filter(
                Q(student_name__icontains = search) | 
                Q(phone_number__icontains = search) |
                Q(course__icontains = search) 
            )
        values_for_search['search'] = request.GET.get('search')

    
    if request.GET.get('enroll'):
        if request.GET.get('enroll') == 'enrolled':
            student_objs = student_objs.filter(orders__is_paid = True)
        elif request.GET.get('enroll') == 'un-enrolled':
            student_objs = student_objs.filter(orders__is_paid = False)
        values_for_search['enroll'] = request.GET.get('enroll')


    if request.GET.get('course'):
        student_objs = student_objs.filter(orders__course__package_title__icontains = request.GET.get('course'))


    if request.GET.get('start_date') or  request.GET.get('end_date'):
        values_for_search['start_date'] = request.GET.get('start_date')
        values_for_search['end_date'] = request.GET.get('end_date')

        if request.GET.get('start_date') and  request.GET.get('end_date'):
            start_date = datetime.datetime.strptime(request.GET.get('start_date'), "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(request.GET.get('end_date'), "%Y-%m-%d").date()

            student_objs = student_objs.filter(orders__order_creation_date_time__gte =start_date ,
            orders__order_creation_date_time__lte =end_date , 
            )
        else:
            messages.error(request, 'Both Start and end date are required')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        values_for_search['start_date'] = request.GET.get('start_date')
        values_for_search['end_date'] = request.GET.get('end_date')


    




    if request.GET.get('subject'):
        selected_subjects = request.GET.getlist('subject')
        print(selected_subjects)
        student_objs = student_objs.filter(course__in = selected_subjects)

    if request.GET.get('name'):
        student_objs = student_objs.filter(student_name = request.GET.get('name'))



    page = request.GET.get('page', 1)
    paginator = Paginator(student_objs, 5)
    try:
        student_objs = paginator.page(page)
    except PageNotAnInteger:
        student_objs = paginator.page(1)
    except EmptyPage:
        student_objs = paginator.page(paginator.num_pages)
    
    
    if request.GET.get('type') == 'export':
        student_list = []
        for student_obj in student_objs:
            order_str = ''
            for order in student_obj.orders.all():
                order_str += f'{order.course.package_title} => {order.is_paid} => | '

            if not len(order_str):
                order_str = None

            student_list.append({
                'name' : student_obj.student_name,
                'phone_number' : student_obj.phone_number,
                'whatsapp_number' : student_obj.whatsapp_number,
                'gender' : student_obj.gender,
                'state' : student_obj.state,
                'pincode' : student_obj.pincode,
                'courses_intrested' : student_obj.course,
                'orders' : order_str
            })
        df = pd.DataFrame(student_list)
        file_name = uuid.uuid4()
        df.to_csv(f'public/static/excel/{file_name}.csv' , encoding='UTF-8')
        return redirect(f'/media/excel/{file_name}.csv')


    student_objs = set(student_objs)
    student_objs = list(student_objs)



    return render(request , 'new_dashboard/user/allStudents.html', {'values_for_search' : values_for_search, 'student_objs': student_objs , 'courses' : CoursePackage.objects.all() })


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