from django.urls import path , include
from . import views



urlpatterns = [
   path('', views.CoursesView.as_view()), 
   path('get-chapters/' , views.ChaptersView.as_view()),
   path('get-lessons/' , views.LessonsView.as_view()),
]