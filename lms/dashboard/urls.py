
from django.urls import path , include
from . import views 

urlpatterns = [

   path('students/' , views.students , name="students"),
   path('send-notification/' , views.send_notification , name="send_notification"),
   
  
   #path('login/', views.login , name="login")
]