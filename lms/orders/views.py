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
from django.conf import settings
import razorpay
import sys, os

API_KEY = "test_9f0cd6e73f16fc3b984db1a8d42"
AUTH_TOKEN = "test_77cb05510a342e7be711119f40a"
salt = "2f59120f9f554bb4a9ac68fcab7ae0a9"
api = Instamojo(api_key=API_KEY,auth_token=AUTH_TOKEN,endpoint='https://test.instamojo.com/api/1.1/')


def generate_razorpay_token(amount):
    try:
        KEY_ID = settings.KEY_ID
        KEY_SECRET = settings.KEY_SECRET
        client = razorpay.Client(auth =(KEY_ID , KEY_SECRET))
        payment = client.order.create({'amount':amount * 100, 'currency':'INR',
                              'payment_capture':'1' })
        return payment
    except Exception as e:
        print(e)
    
    return {}

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
                if not course.is_active:
                    return Response({'status' : 400 , 'message' : 'course purchase is ended' })


            except Exception as e:
                print(e)
                return Response({'status' : 400 , 'message' : 'course_uid is invalid' })

            
            # if Order.objects.filter(student = student , course = course , is_paid = True).exists():
            #     return Response({'status' : 400 , 'message' : 'you have already purchased this course' })


            # response = api.payment_request_create(
            # amount=course.selling_price,
            # purpose=f'{course.package_title}',
            # buyer_name=student.student_name,
            # send_email=True,
            # email=student.email,
            # redirect_url="http://13.232.227.45/api/order/success/",
            # )
            razorpay_dict = generate_razorpay_token(course.selling_price)
            print('******')
            print(razorpay_dict)
            print('******')

            order_obj ,_ = Order.objects.get_or_create(
                student= student,
                course = course,
                is_paid = False,
                )
                
            order_obj.order_id = razorpay_dict['id']
            order_obj.amount = course.selling_price
            order_obj.response = json.dumps(razorpay_dict)
            order_obj.save()
            serializer = OrderSerializer(order_obj)
            data = serializer.data
            #data.pop('response')
            payload_dict = {
                'status' : 200,
                'message' : 'order created',
                'order' : razorpay_dict,
                'data' : serializer.data,
                'razorpay_key' : settings.KEY_ID 
                           }
            # payload = response
            # payload['order'] = razorpay_dict
            #print(response)
            return Response( payload_dict)
        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
        return Response({'status': 400 , 'message' : 'something went wrong'})


    def patch(self , request):
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

            actual_amount  = order_obj.course.selling_price
            order_obj.amount = actual_amount
            order_obj.coupon = None
            order_obj.save()

            course = order_obj.course
            student = order_obj.student
            order_obj = Order.objects.filter(
                student= student,
                course = course,
                is_paid = False,
                ).first()

            # response = api.payment_request_create(
            # amount=order_obj.amount,
            # purpose=f'{course.package_title}',
            # buyer_name=student.student_name,
            # send_email=True,
            # email=student.email,
            # redirect_url="http://13.232.227.45/api/order/success/",
            # )
            razorpay_dict = generate_razorpay_token(order_obj.amount)

            order_obj.response = json.dumps(razorpay_dict)
            order_obj.order_id = razorpay_dict['id']
            order_obj.save()
            serializer = OrderSerializer(order_obj)
          
            payload_dict = {
                'status' : 200,
                'message' : 'coupon removed',
                'order' : razorpay_dict,
                'data' : serializer.data,
                'razorpay_key' : settings.KEY_ID 
                }
    

            return Response(payload_dict)
        except Exception as e:
            print(e)
        return Response({
                'status' : 200,
                'message' : 'coupon removed',
                'data' : {}
            })

class OrderSuccess(APIView):
    def get(self,request):
        import datetime
        try:
            payment_id = request.GET.get('payment_id')
            order_id = request.GET.get('order_id')
            payment_request_id = request.GET.get('payment_request_id')

            order_obj = Order.objects.get( 
                order_id = order_id
            )
        

            order_obj.is_paid = True
            order_obj.payement_id = payment_id
            count_days = None
            if order_obj.course.subscription_type == 'Fixed Date':
                to_date = datetime.date.today() + datetime.timedelta(days=order_obj.course.days)
                order_obj.order_expiry = to_date
            else:
                order_obj.order_expiry  = order_obj.course.sell_till_date

            if order_obj.coupon :
                CouponUsedBy.objects.create(
                    coupon = order_obj.coupon,
                    student = order_obj.student,
                    is_applied = True
                )




            order_obj.save()

            return Response({'status' : 200 , 'message' : 'Payment successfull'})



        except Exception as e:
            print(e)
        
        return Response({'status' : 400 , 'message' : 'Something went wrong may be payment already done'} )
    def post(request):
        print(request.data)



class OrderAPI(APIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


    def get(self , request):
        try:
            phone_number = request.GET.get('phone_number')
            orders = Order.objects.filter(student__phone_number = phone_number , is_paid =False).first()
            serializer = OrderSerializer(orders)
            return Response({'status' : 200 , 'data' : serializer.data , 'message' : 'active order'})


            
        except Exception as e:
            print(e)
        
        return Response({'status' : 400 , 'data' : [] , 'message' : 'Someting went wrong add phone_number key'})

from datetime import date, datetime

class ApplyCoupon(APIView):
    def post(self , request):
        try:
            data = request.data
            print(data)
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
            if order_obj.coupon:
                serializer = OrderSerializer(order_obj)
                data = serializer.data
                # data.pop('response')
                # payload = response
                # payload['order'] = data
                return Response({
                    'status' : 400,
                    'message' : 'coupon is already applied',
                    'data' :data
                })


            if not coupon_obj.is_active:
                return Response({
                    'status':400,
                    'message' : 'invalid coupon code'
                })
            import datetime
            
            try:
                if coupon_obj.coupon_validity:
                    current_date = datetime.date.today()
                    coupon_date =  coupon_obj.coupon_validity.split('T')
                    coupon_date = coupon_date[0]
                    print(coupon_date)
                    print(current_date)
                    d1 = datetime.datetime.strptime(coupon_date, "%Y-%m-%d").date()
                    print(d1)
                    if current_date > d1:
                        return Response({
                            'status':400,
                            'message' : ' coupon code expired'
                        })

            except Exception as e:
                print(e)
                
            if CouponUsedBy.objects.filter(student = order_obj.student,coupon = coupon_obj).count() > coupon_obj.per_user_limit:
                return Response({
                    'status':400,
                    'message' : 'you have exhausted coupon limit'
                })


            if CouponUsedBy.objects.filter(coupon = coupon_obj).count() > coupon_obj.total_usage_limit :
                return Response({
                    'status':400,
                    'message' : 'coupon limit expired'
                })
              


            if not coupon_obj.courses.filter(uid__in = [order_obj.course.uid]).exists():
                return Response({
                        'status':400,
                        'message' : "coupon can't be applied to this course "
                    })
            

            order_obj.coupon = coupon_obj
            
            if coupon_obj.discount_type == 'Fixed Discount':
                order_obj.amount =  order_obj.amount - coupon_obj.discount
                order_obj.save()
                print('Fixed Discount APPLIED')
            else:
                amount_to_be_less = 100 #(order_obj.amount / coupon_obj.discount) * 100
                print(amount_to_be_less)
                amount= 0
                discount_amount= 0
                pay_amount = 0
                discount_amount =  order_obj.amount * coupon_obj.discount / 100   
                pay_amount = order_obj.amount  - discount_amount
                order_obj.amount =  pay_amount
                order_obj.save()
                print('Percentage APPLIED')
                print(order_obj.amount)
                print('Percentage APPLIED')

            course = order_obj.course
            student = order_obj.student
            
            order_obj  = Order.objects.get(uid = data.get('order_id'))

            print('***************')
            print(type(order_obj.amount))
            print('***************')
            if order_obj.amount > 0:
                razorpay_dict = generate_razorpay_token(order_obj.amount)

                # response = api.payment_request_create(
                # amount= order_obj.amount,
                # purpose=f'{course.package_title}',
                # buyer_name=student.student_name,
                # send_email=True,
                # email=student.email,
                # redirect_url="http://13.232.227.45/api/order/success/",
                # )
                order_obj.response = json.dumps(razorpay_dict)
                order_obj.order_id = razorpay_dict['id']
                order_obj.save()
                serializer = OrderSerializer(order_obj)
                data = serializer.data
                payload_dict = {
                    'status' : 200,
                    'message' : 'coupon applied',
                    'order' : razorpay_dict,
                    'data' : serializer.data,
                    'razorpay_key' : settings.KEY_ID 
                }

                # payload = razorpay_dict

                # payload['order'] = data
            else:
                order_obj.is_paid = True
                order_obj.save()
                return Response({
                'status' : 200,
                'message' : 'coure purchased',
                'data' : {}
                 })

    


            return Response(payload_dict)
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



