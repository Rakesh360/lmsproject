from django.db.models import manager
from django.shortcuts import render
from rest_framework import serializers

from rest_framework.views import APIView

from .models import *
from .serializers import *
from rest_framework.response import Response


class CoursesView(APIView):

    def get(self , request):
        course_objs = Course.objects.all()
        print(course_objs)
        serializer = CourseSerializer(course_objs , many=True)
     
        return Response({'status' : 200 , 'data' :serializer.data})
