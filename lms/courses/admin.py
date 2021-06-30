from django.contrib import admin
from .models import *
from django.forms import CheckboxSelectMultiple
@admin.register(CourseDiscount)
class CourseDiscountAdmin(admin.ModelAdmin):
    list_display = ['discount' , 'to_be_applied']

@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    pass









@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        'course_bundle_category',
        'is_active',
        'course_bundle_name','course_bundle_price','course_bundle_discount']
    