from django.urls import path , include
from . import views



urlpatterns = [
   path('', views.CoursesView.as_view()), 
   path('live/<id>/' , views.live_stream_view),
   path('add-course/' , views.add_course, name="add_course")
]
