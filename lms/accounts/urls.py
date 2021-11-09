from django.urls import path , include
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register("", views.AccountViewSet, basename="site-survey")



urlpatterns = [
   path('login/' , views.login_view , name="login_view"),
   path('block_account/<uid>/' , views.block_account , name="block_account"),
   path('', include(router.urls)), 
]
