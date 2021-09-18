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

    def check_in_package(self):
        return CoursePackageSubjects.objects.filter(subject = self).exists()


    class Meta:
        db_table = "subject"
        verbose_name_plural = "Course Subject"
        ordering = ['-created_at']


class SubjectChapters(BaseModel):
    subject = models.ForeignKey(Subject ,related_name="subject_chapters", null=True , blank=True , on_delete=models.CASCADE)
    chapter_title = models.CharField(max_length=100 , null=True , blank=True)

    
    def __str__(self) -> str:
        return self.chapter_title

    class Meta:
        db_table = "course_chapters"
        verbose_name_plural =  "Subject chapters"
        ordering = ['-created_at']


class Quiz(BaseModel):
    pass

class Video(BaseModel):
    video_uploaded_on = models.CharField(choices = (('Vimeo' , 'Vimeo') , ('Youtube' , 'Youtube')) , null=True , blank=True , max_length=100)
    video_link = models.URLField(null=True , blank=True)
    
class Document(BaseModel):
    document_file = models.FileField(upload_to='documents')



class Lessons(BaseModel):
    LESSON_TYPE = (('Video' , 'Video') , ('Document' , 'Document'), ('Video + Document' , 'Video + Document') , ('Quiz' , 'Quiz'))
    VIDEO_PLATFORM = (('Youtube', 'Youtube') , ('Live' , 'Live') , ('Vimeo' , 'Vimeo'))
    lesson_title = models.CharField(max_length=100 )
    #subject = models.ForeignKey(Subject , on_delete=models.CASCADE)
    chapter = models.ForeignKey(SubjectChapters , related_name='subject_lessons', on_delete=models.CASCADE)
    lesson_type = models.CharField(max_length=100 , choices=LESSON_TYPE, default='Video') 
    video_platform = models.CharField(max_length=100 , choices=VIDEO_PLATFORM ,default='Youtube')
    is_free = models.BooleanField(default=False)

    document = models.ForeignKey(Document , on_delete=models.SET_NULL , null=True , blank=True)
    video = models.ForeignKey(Video , on_delete=models.SET_NULL , null=True , blank=True)


    def __str__(self) -> str:
        return self.lesson_title
   
    class Meta:
        db_table = "lesson_chapters"
        verbose_name_plural =  "Lesson chapters"
        ordering = ['-created_at']




class CoursePackage(BaseModel):
    package_title = models.CharField(max_length=100)
    package_description = models.TextField()
    actual_price = models.IntegerField()
    selling_price = models.IntegerField()
    package_type = models.CharField(max_length=100, default='Fixed Date' , choices=(('Fixed Date' , 'Fixed Date') , ('Subscription' , 'Subscrption')))
    days = models.IntegerField(default=0)
    sell_till = models.DateField(null=True , blank=True ,  max_length=100)
    is_active = models.BooleanField(default=True)
    web_image = models.ImageField(upload_to = "course_package",)
    mobile_image = models.ImageField(upload_to = "course_package")

    class Meta:
        db_table = "course_package"
        verbose_name_plural =  "Course Package"
        ordering = ['-created_at']



class CoursePackageSubjects(BaseModel):
    course_package = models.ForeignKey(CoursePackage,related_name='pacakge_subjects', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject  , on_delete=models.CASCADE)
    s_no = models.IntegerField(default=1)
    def __str__(self) -> str:
        return self.subject.subject_title

class CoursePackageChapters(BaseModel):
    course_package_subject = models.ForeignKey(CoursePackageSubjects , related_name='pacakge_subject_chapters',on_delete=models.CASCADE)
    subject_chapter = models.ForeignKey(SubjectChapters , on_delete=models.CASCADE)
    s_no = models.IntegerField(default=1)
    
    def __str__(self) -> str:
        return self.subject_chapter.chapter_title

class CoursePackageLessons(BaseModel):
    course_package_chapter = models.ForeignKey(CoursePackageChapters , related_name='pacakge_subject_chapters_lessons',on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lessons , on_delete=models.CASCADE)
    s_no = models.IntegerField(default=1)

    def __str__(self) -> str:
        return self.lesson.lesson_title
    

class GoLive(BaseModel):
    from datetime import datetime
    course_package = models.ForeignKey(CoursePackage , related_name='live' , on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject , on_delete=models.CASCADE)
    chapter = models.ForeignKey(SubjectChapters , on_delete=models.CASCADE)
    live_name = models.CharField(max_length=100)
    live_url = models.CharField(max_length=10000)
    image = models.ImageField(upload_to = 'live' , null=True , blank = True)
    live_date_time = models.DateTimeField(default=datetime.now)






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
    



class Coupoun(BaseModel):
    coupon_code = models.CharField(max_length=100 , unique=True)
    # coupon_type = models.ManyToManyField(choices=(
    #     ('One time' , 'One time'),
    #     ('Validity' , 'Validity'),
    #     ('Specific Course','Specific Course')), to = choices)

    courses = models.ManyToManyField(CoursePackage)
    start_date = models.DateField(null=True , blank=True)
    expiry_date = models.DateField(null=True , blank=True)

    coupon_discount_type = models.CharField(max_length=100 , choices=(('Percentage' ,'Percentage') , ('Amount' , 'Amount')))
    discount =  models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.coupon_code

    class Meta:
        db_table = "coupons"
        verbose_name_plural = "Coupon "
        ordering = ['-created_at']


    
    


