from django.db.models import manager
from django.shortcuts import render
from rest_framework import serializers
from rest_framework import authentication
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from base_rest.viewsets import BaseAPIViewSet
from instamojo_wrapper import Instamojo
import json

API_KEY = "test_9f0cd6e73f16fc3b984db1a8d42"
AUTH_TOKEN = "test_77cb05510a342e7be711119f40a"
salt = "2f59120f9f554bb4a9ac68fcab7ae0a9"
api = Instamojo(api_key=API_KEY,auth_token=AUTH_TOKEN,endpoint='https://test.instamojo.com/api/1.1/')



class OrderCourse(APIView):
    def post(self , request):
        response = {'status': 400 , 'message' : 'something went wrong'}
        try:
            data = request.data
            if data.get('course_uid') is None:
                return Response({'status' : 400 , 'message' : 'course_uid is required' })
            if data.get('phone_number') is None:
                return Response({'status' : 400 , 'message' : 'phone_number is required' })
            student = None
            try:
                student = Student.objects.get(phone_number = data.get('phone_number'))
            except Exception as e:
                print(e)
                return Response({'status' : 400 , 'message' : 'phone_number is invalid' })
            
            course = None
            try:
                course = CoursePackage.objects.get(uid = data.get('course_uid'))
            except Exception as e:
                print(e)
                return Response({'status' : 400 , 'message' : 'course_uid is invalid' })


            response = api.payment_request_create(
            amount=course.selling_price,
            purpose='Buying course',
            buyer_name=student.student_name,
            send_email=True,
            email=student.email,
            redirect_url="http://13.232.227.45/api/order/success/",
            )
            order_obj = Order.objects.get_or_create(
                student= student,
                course = course,
                is_paid = False,
                order_id = response['payment_request']['id'],
                amount = course.selling_price,
                response = json.dumps(response)
                )
            print(response)

        except Exception as e:
            print(e)
        
        return Response(response)


class OrderSuccess(APIView):
    def get(self,request):
        try:
            payment_id = request.GET.get('payment_id')
            payment_request_id = request.GET.get('payment_request_id')
            order_obj = Order.objects.get( 
                order_id = payment_request_id
            )
            order_obj.is_paid = True
            order_obj.payement_id = payment_id
            order_obj.save()

            return Response({'status' : 200 , 'message' : 'Payment successfull'})



        except Exception as e:
            print(e)
    def post(request):
        print(request.data)



class OrderAPI(BaseAPIViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self , request):
        try:
            print(request.user.student)
            orders = Order.objects.filter(student = request.user.student)
            
        except Exception as e:
            print(e)
        
        return Response({'status' : 200 , 'data' : [] , 'message' : 'Someting went wrong'})

