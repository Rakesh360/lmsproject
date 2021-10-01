from django.db import models
from base_rest.models import *
from django.contrib.auth.models import User
from courses.models import *

class NotificationManager(BaseModel):
    fcm_token = models.TextField()



class Student(User):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_logged_in = models.BooleanField(default=False)
    fcm_token = models.TextField(null=True , blank=True)
    student_name = models.CharField(max_length=100 , null=True , blank=True)
    phone_number = models.CharField(unique=True , max_length=12 , null=True , blank=True)
    whatsapp_number = models.CharField(max_length=12 , null=True , blank=True)
    date_of_birth = models.CharField(max_length=100, null=True , blank=True)
    gender = models.CharField(max_length=100 , choices=(('Male' , 'Male') , ('Female', 'Female'), ('Not to say' , 'Not to sat')) , null=True , blank=True)
    state = models.CharField(max_length=100 , null=True , blank=True)
    district = models.CharField(max_length=100 , null=True , blank=True)
    pincode = models.CharField(max_length=100 , null=True , blank=True)
    accepted_terms = models.BooleanField(default=True)
    
    course = models.CharField(max_length=100 , default='')
    otp = models.CharField(max_length=8 , null=True , blank=True)
    is_phone_verified = models.BooleanField(default=True)
    is_email_verified = models.BooleanField(default=True)
    email_verification_token = models.CharField(max_length=200 , null=True, blank=True)
    forget_password_token = models.CharField(max_length=200 ,null=True, blank=True)
    last_login_time = models.DateTimeField(null=True, blank=True)
    last_logout_time = models.DateTimeField(null=True, blank=True)
    

    def __str__(self) -> str:
        return f'{self.student_name} | {self.email} | {self.phone_number}' 

    class Meta:
        db_table = "students"
        verbose_name_plural =  "Students"
        ordering = ['-uid']
