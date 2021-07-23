import courses
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
    subject_chapters = models.ForeignKey(SubjectChapters , related_name='subject_lessons', null=True , blank=True, on_delete=models.CASCADE)
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
    package_description = models.TextField(null=True , blank=True)
    package_image = models.ImageField(upload_to = 'courses',null=True , blank=True)
    subjects = models.ManyToManyField(Subject,null=True , blank=True)
    actual_price = models.IntegerField(null=True , blank=True)
    selling_price = models.IntegerField(default = 0)
    sell_from = models.DateField(null=True , blank=True)
    sell_till = models.DateField(null=True , blank=True)
    is_active = models.BooleanField(default=True)
    course_validity = models.DateField(null=True , blank=True)
    course_package_info = models.TextField(default='[]')
    course_subjects = models.TextField(default='[]')
    course_chapters = models.TextField(default='[]')
    course_lessons = models.TextField(default='[]')
    web_image = models.ImageField(upload_to = "course_package",null=True , blank=True)
    mobile_image = models.ImageField(upload_to = "course_package",null=True , blank=True)

    class Meta:
        db_table = "course_package"
        verbose_name_plural =  "Course Package"
        ordering = ['-created_at']



class CoursePackageSubjects(BaseModel):
    course_package = models.ForeignKey(CoursePackage,related_name='pacakge_subjects', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject  , on_delete=models.CASCADE)


class CoursePackageChapters(BaseModel):
    course_package_subject = models.ForeignKey(CoursePackageSubjects , related_name='pacakge_subject_chapters',on_delete=models.CASCADE)
    subject_chapter = models.ForeignKey(SubjectChapters , on_delete=models.CASCADE)

class CoursePackageLessons(BaseModel):
    course_package_chapter = models.ForeignKey(CoursePackageChapters , related_name='pacakge_subject_chapters_lessons',on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lessons , on_delete=models.CASCADE)
    sequence = models.IntegerField(default=1)


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
    