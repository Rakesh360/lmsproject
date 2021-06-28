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


@admin.register(CourseChapters)
class CourseChaptersAdmin(admin.ModelAdmin):
    model = CourseChapters
    inlines = [LessonsAdmin]



@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_category' ,'course_title', 'course_price', 'course_level']
    ordering = ('-created_at', )


@admin.register(CourseBundle)
class CourseBundleAdmin(admin.ModelAdmin):
    list_display = ['course_bundle_name','course_bundle_price','course_bundle_discount']
    # formfield_overrides = {
    #     models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    # }