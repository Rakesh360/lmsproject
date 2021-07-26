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
   path('course-packages/' , views.course_packages, name="course_packages"),
   path('add-package/' , views.add_package , name="add_package"),
   path('add-subjects-package/<uid>/' , views.add_subjects_courses,name="add_subjects_courses"),
   path('get-chapters/' , views.ChaptersView.as_view()),
   path('get-lessons/' , views.LessonsView.as_view()),
   path('save-course-package/' , views.SaveCoursePackage.as_view())
]
