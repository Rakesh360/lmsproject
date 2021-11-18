from django.urls import path , include
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register("", views.AccountViewSet, basename="site-survey")



urlpatterns = [
   path('phone-verification/' , views.PhoneNumbersView.as_view()),
   path('verify-phone/' , views.VerifyPhone.as_view()),
   path('', include(router.urls)),
]
