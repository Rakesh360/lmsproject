from django.db.models import fields
from rest_framework import serializers
from base_rest.utils import *
from .models import *

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'