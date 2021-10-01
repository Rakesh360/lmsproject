from django.db.models import fields
from rest_framework import serializers
from base_rest.utils import *
from .models import *
from courses.serializers import CoupounSerializer

class OrderSerializer(serializers.ModelSerializer):
    coupon = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = '__all__'
    
    def get_coupon(self , obj):
        try:
            print(obj.coupon)
            if obj.coupon:
                serializer = CoupounSerializer(obj.coupon)
                return serializer.data
            return None

        except Exception as e:
            return None
    