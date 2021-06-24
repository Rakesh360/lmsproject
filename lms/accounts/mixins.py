
import re
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
import uuid
from .models import *
from rest_framework.authtoken.models import Token

from .serializers import (  LoginSerializer,
                            PasswordSerializer,
                            UserSerializer , ForgetPasswordSerializer)
from django.contrib.auth import get_user_model


class AccountMixin:
    
    @action(detail=False, methods=['post'] ,url_path="login" ,url_name="login"  )
    def login(self , request):
       try:
            data = request.data
            if data.get('email') is None or data.get('password') is None:
                return Response( {'staus' :400 , 'message' : 'email and password both are requied' , 'errors' : []})
            
            # student = Student.objects.filter(email = data.get('email'))
            # if not student.exists():
            #     return Response( {'staus' :400 , 'message' : 'account not found' , 'errors' : []})
            
            print(data.get('email'))
            student = Student.objects.first()
            print(student.check_password(data.get('password')))

            student_obj = authenticate(email = data.get('email') , password = data.get('password'))

            # if not student_obj:
            #     return Response( {'staus' :400 , 'message' : 'invalid password' , 'errors' : []})

            token,_ = Token.objects.get_or_create(user=student_obj)
            print(token)
            return Response({'staus' :200 , 'message' : 'login successfull' , 'token' :'' })


       except Exception as e:
           print(e)
    
    
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
                user_obj = User.objects.get(uid = pk)
                if user_obj.otp == data.get('otp'):
                    user_obj.is_phone_verified = True
                    user_obj.save()
                    return Response( {'staus' :200 , 'message' : 'OTP matched' , 'errors' : []} )
                else:
                    return Response( {'staus' :400 , 'message' : 'you have entered a wrong OTP' , 'errors' : []} )

            except Exception as e:

                return Response( {'staus' :400 , 'message' : 'invalid id'} )



        except Exception as e:
            print(e)
        
        return Response( {'staus' :400 , 'message' : 'something went wrong'} )




    
    @action(detail=False , methods=['put'] , url_path="change-password" ,url_name="change-password")
    def change_password(self,request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.change_password() 
        response = {'staus' : 200 , 'message' : 'Password changed'}
        return Response(response , status.HTTP_200_OK)