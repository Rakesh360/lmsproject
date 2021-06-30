from django.contrib import admin
from .models import Coupoun


@admin.register(Coupoun)
class CoupounAdmin(admin.ModelAdmin):
    list_display = ['coupon_code', 'coupon_type', 'coupon_discount_type', 'discount', 'is_active']