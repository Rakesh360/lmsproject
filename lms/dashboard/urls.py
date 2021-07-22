
from django.urls import path , include
from . import views 

urlpatterns = [
   path('' , views.dashboard , name="dashboard"),
   path('students/' , views.students , name="students"),
   path('addpackages/' , views.addpackages , name="addpackages"),
   path('allpackages/' , views.allpackages , name="allpackages"),
   path('addvideos/' , views.addvideos , name="addvideos"),
   path('allvideos/' , views.allvideos , name="allvideos"),
   path('allsubjects/' , views.allsubjects , name="allsubjects"),
   path('addsubjects/' , views.addsubjects , name="addsubjects"),
   path('login/', views.login , name="login")
]