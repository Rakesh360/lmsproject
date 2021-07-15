from django.contrib import admin
from .models import *
from django.forms import CheckboxSelectMultiple
@admin.register(CourseDiscount)
class CourseDiscountAdmin(admin.ModelAdmin):
    list_display = ['discount' , 'to_be_applied']

@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    pass



class LessonsAdmin(admin.StackedInline):
    model = Lessons


@admin.register(SubjectChapters)
class SubjectChaptersAdmin(admin.ModelAdmin):
    inlines = [ LessonsAdmin ]
    list_display = ['chapter_title' , 'subject', 'total_lessons' , 'created_at' , 'updated_at']

    def total_lessons(self , obj):
        return Lessons.objects.filter(subject_chapters = obj).count()

class SubjectChapterAdmin(admin.StackedInline):
    model = SubjectChapters

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    inlines = [ SubjectChapterAdmin ]
    list_display = ['subject_title' ,'subject_category' , 'total_chapters' , 'created_at' , 'updated_at']

    def total_chapters(self , obj):
        return SubjectChapters.objects.filter(subject = obj).count()



@admin.register(Lessons)
class LessonAdmin(admin.ModelAdmin):
    pass



@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        'course_bundle_category',
        'is_active',
        'course_bundle_name','course_bundle_price','course_bundle_discount']
    

admin.site.register(LiveStream)