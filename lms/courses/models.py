from django.db import models
from base_rest.models import BaseModel
from froala_editor.fields import FroalaField
from django.utils.text import slugify 



class CourseDiscount(BaseModel):
    discount = models.IntegerField(default=0)
    to_be_applied = models.BooleanField(default=False)

class CourseCategory(BaseModel):
    category_name = models.CharField(max_length=100)
    category_image = models.FileField(upload_to = 'category')


class Course(BaseModel):
    course_category = models.ForeignKey(CourseCategory , on_delete=models.CASCADE , null=True , blank=True)
    course_title = models.CharField(max_length=100)
    course_slug = models.SlugField(null=True , blank =True)
    enrolled_students = models.IntegerField(default=100)
    course_price = models.IntegerField(default=100)
    course_image = models.ImageField(upload_to = 'courses')
    course_upload_on = models.CharField(max_length=100 ,choices=(('Vimeo' , 'Vimeo') , ('Youtube' , 'Youtube')) , default='Vimeo')
    discount_price = models.IntegerField(default=0)
    course_description = FroalaField()
    course_level = models.CharField(max_length=100 ,
        choices=(('Beginner' , 'Beginner' ),
                ('Intermediate' ,'Intermediate') , ('Advanced' , 'Advanced')) , default='Intermediate')

    def __str__(self) -> str:
        return self.course_title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.course_title)
        super(Course, self).save(*args, **kwargs)





class CourseChapters(BaseModel):
    course = models.ForeignKey(Course , related_name='course' , on_delete=models.CASCADE)
    chapter_title = models.CharField(max_length=100 , null=True , blank=True)
    chapter_type = models.CharField(max_length=100 ,
        choices=(('Lesson' , 'Lesson' ) , ('Code' , 'Code') , ('MCQ' , 'MCQ')))

    def __str__(self) -> str:
        return self.course.course_title

class Lessons(BaseModel):
    course_chapters = models.ForeignKey(CourseChapters , related_name='course_chapters' , on_delete=models.CASCADE)
    video_link = models.URLField()
    lesson_title = models.CharField(max_length=100 , null=True , blank=True)

    can_watch = models.BooleanField(default=False)
    video_duration = models.CharField(max_length=30)
   

