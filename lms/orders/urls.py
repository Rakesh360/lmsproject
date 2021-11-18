

from django.urls import path , include
from . import views
from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register("", views.OrderAPI, basename="site-survey")

from .views import *

urlpatterns = [
   path('' , OrderCourse.as_view()),
   path('get-active-order/' , OrderAPI.as_view()),
   path('success/' , OrderSuccess.as_view()),
   path('apply-coupon/' , ApplyCoupon.as_view()),
   path('block_access/' , block_access , name="block_access"),
   path('enroll_student/<uid>/' , enroll_student , name="enroll_student")
   #path('', include(router.urls)), 
]


