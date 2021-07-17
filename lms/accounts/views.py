import uuid
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (  LoginSerializer,
                            RegisterStudentSerializer , ForgetPasswordSerializer)

from rest_framework import serializers, status
from base_rest.viewsets import BaseAPIViewSet
from .models import *
from .mixins import AccountMixin



def login_view(request):
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
        if User.objects.last():
            User.objects.last().delete()


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