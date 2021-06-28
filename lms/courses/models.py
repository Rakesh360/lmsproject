from django.db import models
from django.db.models.deletion import SET_NULL
from base_rest.models import BaseModel
from froala_editor.fields import FroalaField
from django.utils.text import slugify 



class CourseDiscount(BaseModel):
    discount = models.IntegerField(default=0)
    to_be_applied = models.BooleanField(default=False)

class CourseCategory(BaseModel):
    category_name = models.CharField(max_length=100)
    category_image = models.FileField(upload_to = 'category')

    def __str__(self) -> str:
        return self.category_name



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


    class Meta:
        db_table = "course_subject"
        verbose_name_plural = "Course Subject"
        ordering = ['-created_at']


class CourseChapters(BaseModel):
    course = models.ForeignKey(Course , related_name='course' , on_delete=models.CASCADE)
    chapter_title = models.CharField(max_length=100 , null=True , blank=True)
    chapter_type = models.CharField(max_length=100 ,
        choices=(('Lesson' , 'Lesson' ) , ('Code' , 'Code') , ('MCQ' , 'MCQ')))

    def __str__(self) -> str:
        return self.course.course_title
    class Meta:
        db_table = "course_chapters"
        verbose_name_plural =  "Subject chapters"
        ordering = ['-created_at']


class Lessons(BaseModel):
    course_chapters = models.ForeignKey(CourseChapters , related_name='course_chapters' , on_delete=models.CASCADE)
    video_link = models.URLField()
    lesson_title = models.CharField(max_length=100 , null=True , blank=True)

    can_watch = models.BooleanField(default=False)
    video_duration = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.lesson_title
   
    class Meta:
        db_table = "lesson_chapters"
        verbose_name_plural =  "Lesson chapters"
        ordering = ['-created_at']




class CourseBundle(BaseModel):
    course_bundle_category = models.ForeignKey(CourseCategory , on_delete=models.SET_NULL , null=True , blank=True)
    course_bundle_name = models.CharField(max_length=100)
    course_bundle_description = models.CharField(max_length=100)
    course_bundle_image = models.ImageField(upload_to = 'courses')
    courses = models.ManyToManyField(Course)
    course_bundle_price = models.IntegerField()
    course_bundle_discount = models.IntegerField(default = 0)
    class Meta:
        db_table = "course"
        verbose_name_plural =  "Course Bundle"
        ordering = ['-created_at']
