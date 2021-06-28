from django.contrib import admin
from .models import *


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'student',
        'course',
        'amount',
        'is_paid',
        'created_at']