
import re
from rest_framework import exceptions, serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
import uuid
from .models import *
from rest_framework.authtoken.models import Token

from .serializers import ( ChangePasswordSerializer, LoginSerializer,
                            PasswordSerializer,
                            StudentSerializer,RegisterStudentSerializer , ForgetPasswordSerializer)
from django.contrib.auth import get_user_model


class AccountMixin:
    
    @action(detail=False, methods=['post'] ,url_path="login" ,url_name="login"  )
    def login(self , request):
       try:
            data = request.data
            if data.get('email') is None or data.get('password') is None:
                return Response( {'staus' :400 , 'message' : 'email and password both are requied' , 'errors' : []})
            
            student = Student.objects.filter(email = data.get('email'))
            if not student.exists():
                return Response( {'staus' :400 , 'message' : 'account not found' , 'errors' : []})
            
            if not student[0].is_phone_verified:
                return Response( {'staus' :400 , 'message' : 'your phone is not verified' , 'errors' : []})



            student_obj = authenticate(username = data.get('email') , password = data.get('password'))

            if not student_obj:
                return Response( {'staus' :400 , 'message' : 'invalid password' , 'errors' : []})

            token,_ = Token.objects.get_or_create(user=student_obj)
            
            student_serializer = StudentSerializer(student_obj)
            return Response({
                'staus' :200,
                'message' : 'login successfull',
                'token' :str(token), 
                'student' : student_serializer.data })


       except Exception as e:
           print(e)
    
       return Response({'staus' :400 , 'message' : 'Something went wrong' })

    
    
    @action(detail=False, methods=['post'] , url_path="reset" ,url_name="reset")
    def reset(self , request):
        serializer = ForgetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.forget_password()
        response =   {'status': 200 , 'message': 'An email is sent to you' }
        return Response(response , status.HTTP_200_OK)
    
    @action(detail=True , methods=['post'])
    def verify_otp(self , request ,pk):
        try:
            data = request.data
            try:
                student_obj = Student.objects.get(uid = pk)
                if student_obj.otp == data.get('otp'):
                    student_obj.is_phone_verified = True
                    student_obj.save()
                    return Response( {'staus' :200 , 'message' : 'OTP matched account activated' , 'errors' : []} )
                else:
                    return Response( {'staus' :400 , 'message' : 'you have entered a wrong OTP' , 'errors' : []} )

            except Exception as e:

                return Response( {'staus' :400 , 'message' : 'invalid id'} )



        except Exception as e:
            print(e)
        
        return Response( {'staus' :400 , 'message' : 'something went wrong'} )




    
    @action(detail=False , methods=['post']  ,url_name="change-password")
    def change_password(self,request):
        serializer = ChangePasswordSerializer(data=request.data)
        print('aaaaaa')
        if serializer.is_valid():
            student_uid = serializer.data['student_uid']
            new_password = serializer.data['new_password']
            old_password = serializer.data['old_password']
            try:
                student_obj = Student.objects.get(uid = student_uid)
                student_obj = authenticate(username =student_obj.email , password =old_password)

                if student_obj is None:
                    return Response({'status' : 400 , 'message' : 'invalid password'})
                else:
                    student_obj.set_password(new_password)
                    student_obj.save()
                    return Response({'status' : 200 , 'message' : 'password changed'})


            except Exception as e:
                return Response({'status' : 400 , 'message' : 'invalid uid'})

        return Response({'status' : 400 ,'erros' : serializer.errors})

            
        response = {'staus' : 200 , 'message' : 'Password changed'}
        return Response(response , status.HTTP_200_OK)