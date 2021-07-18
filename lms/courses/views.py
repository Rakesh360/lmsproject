from django.db.models import manager
from django.shortcuts import redirect, render
from rest_framework import serializers

from rest_framework.views import APIView

from .models import *
from .serializers import *
from rest_framework.response import Response
from django.contrib import messages
from django.http import HttpResponseRedirect



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


class CoursesView(APIView):

    def get(self , request):
        course_objs = Course.objects.all()
        print(course_objs)
        serializer = CourseSerializer(course_objs , many=True)
     
        return Response({'status' : 200 , 'data' :serializer.data})




def live_stream_view(request , id):
    context = {'live' : LiveStream.objects.get(uid = id)}
    return render(request , 'live.html' , context)