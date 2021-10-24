from django.db.models import fields
from rest_framework import serializers
from base_rest.utils import *
from .models import *
from courses.serializers import CoupounOrderSerializer


class OrderSerializer(serializers.ModelSerializer):
    coupon = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        exclude = [ 'updated_at',]
    
    def get_coupon(self , obj):
        try:
            print(obj.coupon)
            if obj.coupon:
                serializer = CoupounOrderSerializer(obj.coupon)
                return serializer.data
            return None

        except Exception as e:
            return None
    