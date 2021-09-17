from django.urls import path , include
from . import views



urlpatterns = [
   path('', views.CoursesView.as_view()), 
   path('get-chapters/' , views.ChaptersView.as_view()),
   path('lessons/' , views.LessonsView.as_view()),
   path('save-course-package/' , views.SaveCoursePackage.as_view()),

]
