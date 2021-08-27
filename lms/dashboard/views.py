from django.shortcuts import redirect, render
from accounts.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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

    return render(request , 'students/students.html', {'subjects' : subjects, 'student_objs': student_objs })


def send_notification(request):
    return render(request , 'students/send_notification.html')


def export_student_list(request):
    return 