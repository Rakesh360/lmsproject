from django.db import models
from base_rest.models import BaseModel
from froala_editor.fields import FroalaField



class CourseDiscount(BaseModel):
    discount = models.IntegerField(default=0)
    to_be_applied = models.BooleanField(default=False)




class Subject(BaseModel):
    subject_title = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.subject_title


    class Meta:
        db_table = "subject"
        verbose_name_plural = "Course Subject"
        ordering = ['-created_at']


class SubjectChapters(BaseModel):
    subject = models.ForeignKey(Subject , null=True , blank=True , on_delete=models.CASCADE)
    chapter_title = models.CharField(max_length=100 , null=True , blank=True)

    
    def __str__(self) -> str:
        return self.chapter_title

    class Meta:
        db_table = "course_chapters"
        verbose_name_plural =  "Subject chapters"
        ordering = ['-created_at']


class Lessons(BaseModel):
    subject_chapters = models.ForeignKey(SubjectChapters, null=True , blank=True, on_delete=models.CASCADE)
    lesson_title = models.CharField(max_length=100 , null=True , blank=True)
    video_uploaded_on = models.CharField(choices = (('Vimeo' , 'Vimeo') , ('Youtube' , 'Youtube')) , null=True , blank=True , max_length=100)
    video_link = models.URLField(null=True , blank=True)
    
    def __str__(self) -> str:
        return self.lesson_title
   
    class Meta:
        db_table = "lesson_chapters"
        verbose_name_plural =  "Lesson chapters"
        ordering = ['-created_at']




class CoursePackage(BaseModel):
    package_title = models.CharField(max_length=100)
    package_description = FroalaField()
    package_image = models.ImageField(upload_to = 'courses')
    subjects = models.ManyToManyField(Subject)
    actual_price = models.IntegerField()
    selling_price = models.IntegerField(default = 0)
    sell_from = models.DateField()
    sell_till = models.DateField()
    is_active = models.BooleanField(default=True)
    course_validity = models.DateField()
    course_package_info = models.TextField(default='[]')
    web_image = models.ImageField(upload_to = "course_package")
    mobile_image = models.ImageField(upload_to = "course_package")

    class Meta:
        db_table = "course_package"
        verbose_name_plural =  "Course Package"
        ordering = ['-created_at']

# [
# {
#     'subject' : 'Subject name',
#     'subject_chapters' : [
#         {
#             'chaper_name' : 'Chapter name',
#             'lessons' : [

#             ]
#         }
#     ]
# }
# ]

class LiveStream(BaseModel):
    live_stream_link = models.TextField()
    