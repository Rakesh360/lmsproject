
from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (  LoginSerializer,
                            RegisterStudentSerializer,StudentSerializer , ForgetPasswordSerializer)

from rest_framework import status
from base_rest.viewsets import BaseAPIViewSet
from .models import *
from .mixins import AccountMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from courses.helpers import *
import datetime

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


class PhoneNumbersView(APIView):
    # def get(self , request):
    #     phone_number = request.GET.get('phone_number')
    #     if phone_number:
    #         obj , _ = PhoneNumbers.objects.get_or_create(phone_number = phone_number)
    #         obj.otp = send_otp(phone_number)
    #         obj.save()
    #         return Response({
    #                 'status' : 200 , 'message' : 'Otp sent'
    #         })
        
    #     return Response({'status' : 400 , 'message' : 'phone number is required'})
        
    

    def post(self , request):
        try:
            data = request.data
            phone_number =  data.get('phone_number')
            if phone_number is None:
                return Response({'status' : 400 , 'message' : 'phone number is required'})
            
            obj , _ = PhoneNumbers.objects.get_or_create(phone_number = phone_number)
            obj.otp = send_otp(phone_number)
            obj.save()
            return Response({
                'status' : 200 , 'message' : 'Otp sent'
            })
        except Exception as e:
            return Response({
                'status' : 300,
                'message' : str(e)
            })


class VerifyPhone(APIView):
    def post(self , request):
        try:
            data = request.data
            if data.get('phone_number') is None or data.get('otp') is None:
                return Response( {'staus' :400 , 'message' : 'phone_number and otp both are requied' , 'errors' : []})

            obj = PhoneNumbers.objects.get(phone_number = data.get('phone_number'))
            if obj.otp == data.get('otp'):
                return Response( {'staus' :200 , 'message' : 'verified' , 'errors' : []})

            return Response( {'staus' :400 , 'message' : 'invalid otp' , 'errors' : []})


        except Exception as e:
            return Response({
                'status' : 300,
                'message' : str(e)
            })


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
              

                for order in queryset.orders.filter(is_paid = True , course__sell_till_date__gte = datetime.date.today() ):
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
                for order in queryset.orders.filter(is_paid = True , block_access = False, course__sell_till_date__gte = datetime.date.today()):
                    courses.append(course_to_json([order.course]))
                data['courses'] = courses

                expired_course = []
                for order in queryset.orders.filter(is_paid = True , course__sell_till_date__lte = datetime.date.today()):
                    expired_course.append(order.course.package_title)
                for order in queryset.orders.filter( block_access = True):
                    expired_course.append(order.course.package_title)


                data['expired_course'] = expired_course

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


from dashboard.helpers import *

def block_account(request , uid):
    try:
        student = Student.objects.get(uid = uid)
        student.is_blocked = not student.is_blocked

        if student.is_blocked:
            send_notification_packages(
                [student.fcm_token],
                f'Your account has been blocked contact admin',
                'Please contact admin for this..'
            )
        else:
            send_notification_packages(
                [student.fcm_token],
                f'Your account has been un-blocked.',
                'You can now acces the courses'
            )


        student.save()

        messages.success(request, 'Account status changed')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except Exception as e:
        messages.error(request, 'Something went wron')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


