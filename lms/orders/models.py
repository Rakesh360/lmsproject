from django.db import models
from django.db.models.deletion import CASCADE
from accounts.models import Student
from courses.models import *
from base_rest.models import BaseModel

class Order(BaseModel):
    student = models.ForeignKey(Student , on_delete=models.CASCADE)
    course = models.ForeignKey(Course , on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    razorpay_payement_id = models.CharField(max_length=1000 , null = True , blank=True)
    razorpay_order_id = models.CharField(max_length=1000,  null = True , blank=True)
    razorpay_payment_signature = models.CharField(max_length=100 ,  null = True , blank=True)
    order_creation_date_time = models.DateTimeField(auto_now_add=True)
    order_updation_date_time = models.DateTimeField(auto_now = True)
    