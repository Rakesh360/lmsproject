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
    list_display = ['lesson_title' ,'chapter']


@admin.register(CoursePackageLessons)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['lesson' ,'get_package_name','get_subject_chapter','added_at', 'updated_at' , 'created_at']

    def get_subject_chapter(self , obj):
        return obj.course_package_chapter.subject_chapter

    def get_package_name(self , obj):
        return obj.course_package_chapter.course_package_subject.course_package.package_title

#admin.site.register(Lessons)
admin.site.register(CoursePackage)
#admin.site.register(CoursePackageLessons)
admin.site.register(CoursePackageChapters)
admin.site.register(CoursePackageSubjects)
admin.site.register(Video)
admin.site.register(Document)
admin.site.register(GoLive)
admin.site.register(Coupoun)

