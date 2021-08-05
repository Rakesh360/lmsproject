import uuid
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (  LoginSerializer,
                            RegisterStudentSerializer , ForgetPasswordSerializer)

from rest_framework import serializers, status
from base_rest.viewsets import BaseAPIViewSet
from .models import *
from .mixins import AccountMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login


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
