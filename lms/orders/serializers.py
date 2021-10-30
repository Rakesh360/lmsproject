from django.db.models import fields
from rest_framework import serializers
from base_rest.utils import *
from .models import *
from courses.serializers import CoupounOrderSerializer


class OrderSerializer(serializers.ModelSerializer):
    coupon = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        exclude = [ 'updated_at', 'created_at' , 'order_expiry' , 'order_updation_date_time' , 'order_creation_date_time' , 'razorpay_payment_signature' , 'order_id' , 'payement_id' , 'response']
    
    def get_coupon(self , obj):
        try:
            print(obj.coupon)
            if obj.coupon:
                serializer = CoupounOrderSerializer(obj.coupon)
                return serializer.data
            return None

        except Exception as e:
            return None
    