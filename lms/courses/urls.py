from django.urls import path , include
from . import views



urlpatterns = [
   path('', views.CoursesView.as_view()), 
   path('live/<id>/' , views.live_stream_view),
   path('add-course/' , views.add_course, name="add_course"),
   path('subjects/' , views.subjects, name="subjects"),
   path('subject-chapters/' , views.subject_chapters , name="subject_chapters"),
   path('add-lessons/' , views.add_lessons , name="add_lessons"),
   path('lessons/' , views.lessons, name="lessons"),
   path('add-package/' , views.add_package , name="add_package")

]
