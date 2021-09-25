
from django.urls import path , include
from . import views 

urlpatterns = [
   path('', views.dashboard , name="dashboard"),
   path('notify/' , views.send_noti , name="send_noti"),
   path('students/' , views.students , name="students"),
   path('send-notification/' , views.send_notification , name="send_notification"),
   
  
   #path('login/', views.login , name="login")
]