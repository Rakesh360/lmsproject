from django.db import models
from base_rest.models import BaseModel



class CourseDiscount(BaseModel):
    discount = models.IntegerField(default=0)
    to_be_applied = models.BooleanField(default=False)

class CourseCategory(BaseModel):
    category_name = models.CharField(max_length=100)
    category_image = models.FileField(upload_to = 'category')

    def __str__(self) -> str:
        return self.category_name



class Subject(BaseModel):
    subject_category = models.ForeignKey(CourseCategory , on_delete=models.CASCADE , null=True , blank=True)
    subject_title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return self.subject_title


    class Meta:
        db_table = "course_subject"
        verbose_name_plural = "Course Subject"
        ordering = ['-created_at']


class SubjectChapters(BaseModel):
    subject = models.ForeignKey(Subject , related_name='subject' , on_delete=models.CASCADE)
    chapter_title = models.CharField(max_length=100 , null=True , blank=True)

    def __str__(self) -> str:
        return self.chapter_title

    class Meta:
        db_table = "course_chapters"
        verbose_name_plural =  "Subject chapters"
        ordering = ['-created_at']


class Lessons(BaseModel):
    subject_chapters = models.ForeignKey(SubjectChapters , related_name='course_chapters' , on_delete=models.CASCADE)
    lesson_title = models.CharField(max_length=100 , null=True , blank=True)
    lesson_type = models.CharField(choices=(('Video' , 'Video'),('Document' ,'Document') , ('Video + Document' , 'Video + Document')) , max_length=100)
    video_uploaded_on = models.CharField(choices = (('Vimeo' , 'Vimeo') , ('Youtube' , 'Youtube')) , null=True , blank=True , max_length=100)
    video_link = models.URLField(null=True , blank=True)
    document = models.FileField(null=True , blank=True)
    is_free = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.lesson_title
   
    class Meta:
        db_table = "lesson_chapters"
        verbose_name_plural =  "Lesson chapters"
        ordering = ['-created_at']




class Course(BaseModel):
    course_bundle_category = models.ForeignKey(CourseCategory , on_delete=models.SET_NULL , null=True , blank=True)
    course_bundle_name = models.CharField(max_length=100)
    course_bundle_description = models.TextField()
    course_bundle_image = models.ImageField(upload_to = 'courses')
    subjects = models.ManyToManyField(Subject)
    course_bundle_price = models.IntegerField()
    course_bundle_discount = models.IntegerField(default = 0)
    is_active = models.BooleanField(default=True)

    course_validity = models.DateField()

    class Meta:
        db_table = "course"
        verbose_name_plural =  "Course Bundle"
        ordering = ['-created_at']
