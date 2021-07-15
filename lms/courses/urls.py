from django.urls import path , include
from . import views



urlpatterns = [
   path('', views.CoursesView.as_view()), 
   path('live/<id>/' , views.live_stream_view),
]
