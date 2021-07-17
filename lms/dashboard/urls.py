
from django.urls import path , include
from . import views 

urlpatterns = [
   path('' , views.dashboard , name="dashabord"),
   path('students/' , views.students , name="students"),
]