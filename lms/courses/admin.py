from django.contrib import admin
from .models import *
from django.forms import CheckboxSelectMultiple
from django.contrib.admin import AdminSite




admin.site.register(Subject)


class LessonsAdmin(admin.StackedInline):
    model = Lessons
@admin.register(SubjectChapters)
class SubjectChaperAdmin(admin.ModelAdmin):
    inlines = [LessonsAdmin]




admin.site.register(Lessons)
admin.site.register(CoursePackage)
admin.site.register(CoursePackageLessons)
admin.site.register(CoursePackageChapters)
admin.site.register(CoursePackageSubjects)
