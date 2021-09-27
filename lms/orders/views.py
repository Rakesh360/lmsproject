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
from courses.models import *
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

            
            if Order.objects.filter(student = student , course = course , is_paid = True).exists():
                return Response({'status' : 400 , 'message' : 'you have already purchased this course' })


            response = api.payment_request_create(
            amount=course.selling_price,
            purpose=f'{course.package_title}',
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
            return Response(response)
        except Exception as e:
            print(e)
        
        return Response({'status': 400 , 'message' : 'something went wrong'})


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
        
        return Response({'status' : 400 , 'message' : 'Something went wrong may be payment already done'} )
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

from datetime import date

class ApplyCoupon(APIView):
    def post(self , request):
        try:
            data = request.data

            if data.get('order_id') is None or data.get('coupon_code') is None:
                return Response({
                    'status' : 400,
                    'message' : 'both order id and coupon code are required'
                })
            order_obj = None
            coupon_obj = None
            try:
                order_obj = Order.objects.get(uid = data.get('order_id'))
            except Exception as e:
                print(e)

                return Response({
                    'status' : 400,
                    'message' : 'invalid order_id'
                })

            try:
                coupon_obj = Coupoun.objects.get(coupon_code = data.get('coupon_code'))
            except Exception as e:
                return Response({
                    'status' : 400,
                    'message' : 'invalid coupon code'
                })

            print(coupon_obj)
            if order_obj.coupon and  order_obj.coupon.uid == coupon_obj.uid:
                return Response({
                    'status' : 400,
                    'message' : 'coupon is already applied'
                })


            if not coupon_obj.is_active:
                return Response({
                    'status':400,
                    'message' : 'invalid coupon code'
                })
            
            if coupon_obj.coupon_validity is not None and  str(date.today()) > coupon_obj.coupon_validity:
                return Response({
                    'status':400,
                    'message' : ' coupon code expired'
                })
                
            if coupon_obj.per_user_limit != -1:
                if coupon_obj.applied_user_limit == coupon_obj.per_user_limit:
                    return Response({
                        'status':400,
                        'message' : 'coupon code expired'
                    })
                else:
                    coupon_obj.applied_user_limit = coupon_obj.applied_user_limit + 1
                    coupon_obj.save()
            

            if coupon_obj.total_usage_limit != -1:
                if coupon_obj.applied_total_limit == coupon_obj.total_usage_limit:
                    return Response({
                        'status':400,
                        'message' : 'coupon code expired'
                    })
                else:
                    coupon_obj.applied_total_limit = coupon_obj.applied_total_limit + 1
                    coupon_obj.save()


            if not coupon_obj.courses.filter(uid__in = [order_obj.course.uid]).exists():
                return Response({
                        'status':400,
                        'message' : "coupon can't be applied to this course "
                    })
            

            order_obj.coupon = coupon_obj
            
            if coupon_obj.discount_type == 'Fixed Discount':
                order_obj.amount =  order_obj.amount - coupon_obj.discount
                order_obj.save()
            else:
                amount_to_be_less = 100 #(order_obj.amount / coupon_obj.discount) * 100
                print(amount_to_be_less)
                order_obj.amount =  order_obj.amount - amount_to_be_less
                order_obj.save()

            serializer = OrderSerializer(order_obj)
            return Response({
                'status' : 200,
                'message' : 'coupon applied successfully',
                'data' : serializer.data
            })
        except Exception as e:
            import sys, os
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return Response({
                'status' : 400,
                'message' : 'something went wrong'
            })



