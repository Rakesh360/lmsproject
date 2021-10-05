from django.db import models
from base_rest.models import *
from courses.models import CoursePackage

class NotificationLogs(BaseModel):
    notfication_title = models.CharField(max_length=100)
    notification_content = models.TextField()
    notification_image = models.ImageField(null=True , blank = True , upload_to="notifications")
    courses = models.ManyToManyField(CoursePackage)
    logs = models.TextField(default='{}')

    