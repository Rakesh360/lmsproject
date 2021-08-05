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

