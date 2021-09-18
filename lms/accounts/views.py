import uuid
from django.db.models import manager, query
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (  LoginSerializer,
                            RegisterStudentSerializer,StudentSerializer , ForgetPasswordSerializer)

from rest_framework import serializers, status
from base_rest.viewsets import BaseAPIViewSet
from .models import *
from .mixins import AccountMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from courses.helpers import *

def login_view(request):
    try:
        if request.method == 'POST':
            user_obj = User.objects.get(username = request.POST.get('username'))
            user_obj = authenticate(username = request.POST.get('username') , password = request.POST.get('password'))
            if user_obj and user_obj.is_superuser:

                login(request, user_obj)
                return redirect('/')
            
            raise Exception('Invalid credentials')

    except Exception as e:
        print(e)
        messages.success(request, 'Invalid credentials')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))





    return render(request , 'accounts/login.html')



class AccountViewSet(BaseAPIViewSet , AccountMixin):
    queryset = Student.objects.all()
    model_class = Student
    serializer_class = RegisterStudentSerializer
    instance_name = "student"
    ACTION_SERIALIZERS = {
        'reset': ForgetPasswordSerializer,
        'login': LoginSerializer,
    }

    def list(self , request):
        if request.GET.get('uid'):
            try:
                queryset = Student.objects.get(uid = request.GET.get('uid'))
                data = {}
                serializer = RegisterStudentSerializer(queryset)
                data['student_info'] = serializer.data
                courses = []
                for order in queryset.orders.filter(is_paid = True):
                    courses.append(course_to_json([order.course]))
                data['courses'] = courses

                return Response({'status' : 200 , 'data' : data})
            except Exception as e:
                print(e)
                return Response({'status' : 400 , 'data' : {} , 'message' : 'invalid uid'})

        if request.GET.get('phone_number'):
            try:
                queryset = Student.objects.get(phone_number = request.GET.get('phone_number'))
                serializer = RegisterStudentSerializer(queryset)
                data = {}
                serializer = RegisterStudentSerializer(queryset)
                data['student_info'] = serializer.data
                courses = []
                for order in queryset.orders.filter(is_paid = True):
                    courses.append(course_to_json([order.course]))
                data['courses'] = courses

                return Response({'status' : 200 , 'data' : data})
            except Exception as e:
                print(e)
                import sys, os
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

                return Response({'status' : 400 , 'data' : {} , 'message' : 'invalid phone_number'})




        serializer = RegisterStudentSerializer(Student.objects.all() , many=True)
        return Response({'status' : 200 , 'data' : serializer.data})
 
    def create(self, request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = request.data
            student_obj = Student.objects.filter(email = data.get('email'))

            if student_obj.exists():
                return Response(
                {'status' : 400,
                'message' : 'email is already taken',
                'errors' : []})
            student_obj = Student.objects.filter(phone_number = data.get('phone_number'))
            if student_obj.exists():
                return Response(
                {'status' : 400,
                'message' : 'phone number is already taken',
                'errors' : []})
        
            serializer.save()
            return Response({'staus' : 200 ,'message' : 'account created verify OTP' ,'uid' : serializer.data['uid']} ,status.HTTP_200_OK )
        
        return Response(
            {'status' : 400,
            'message' : 'something went wrong',
            'errors' : serializer.error})


    def patch(self , request):
        try:
            data = request.data
            student_obj = Student.objects.get(uid = data.get('uid'))
            serializer = StudentSerializer(student_obj , data = request.data , partial = True)
            if serializer.is_valid():
                serializer.save()
                                
                return Response({
                    'status' : 200,
                    'message' : 'student updated',
                    'data' : serializer.data
                }) 
            return Response(
            {'status' : 400,
            'message' : 'something went wrong',
            'errors' : serializer.error})
        except Exception as e:
            print(e)
                
            return Response({
                'status' : 400,
                'message' : 'invalid uid',
                'data' : {}
            }) 