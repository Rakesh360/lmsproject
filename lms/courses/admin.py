from django.contrib import admin
from .models import *
from django.forms import CheckboxSelectMultiple
from django.contrib.admin import AdminSite




admin.site.register(Subject)


class LessonsAdmin(admin.StackedInline):
    model = Lessons
@admin.register(SubjectChapters)
class SubjectChaperAdmin(admin.ModelAdmin):
    list_display = ['chapter_title' , 'subject']  
    inlines = [LessonsAdmin]



@admin.register(Lessons)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['lesson_title' ,'subject_chapters']


#admin.site.register(Lessons)
admin.site.register(CoursePackage)
admin.site.register(CoursePackageLessons)
admin.site.register(CoursePackageChapters)
admin.site.register(CoursePackageSubjects)
