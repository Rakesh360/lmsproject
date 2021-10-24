from django.db import models
from base_rest.models import *
from courses.models import CoursePackage
from django.db.models.signals import post_save
from django.dispatch import receiver
from dashboard.helpers import *

from orders.models import Order

class NotificationLogs(BaseModel):
    notfication_title = models.CharField(max_length=100)
    notification_content = models.TextField()
    notification_image = models.ImageField(null=True , blank = True , upload_to="notifications")
    courses = models.ManyToManyField(CoursePackage)
    logs = models.TextField(default='{}')




@receiver(post_save, sender=NotificationLogs)
def send_no(sender, instance, **kwargs):
    print('HELLLLLLLL')
    try:
        registration_ids = set()
        for course in instance.courses.all():
            order_obj = Order.objects.filter(course = course , is_paid = True).first()
            if order_obj:
                registration_ids.add(order_obj.student.fcm_token)

        image =  'http://13.232.227.45/' + str(instance.notification_image)
        registration_ids= list(registration_ids)
        send_notification_packages(registration_ids , 
        instance.notfication_title,
        instance.notification_content,
        image,
        )
        
    
    except Exception as e:
        print(e)



    
