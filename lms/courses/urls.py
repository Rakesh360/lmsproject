from django.urls import path , include
from . import views



urlpatterns = [

   path('live/<id>/' , views.live_stream_view),
   path('add-course/' , views.add_course, name="add_course"),
   path('subjects/' , views.subjects, name="subjects"),
   path('edit-subject/<uid>/' , views.edit_subject , name="edit_subject" ),
   path('edit-subject-chapter/<uid>/' , views.edit_subject_chapter , name="edit_subject_chapter"),
   path('subject-chapters/' , views.subject_chapters , name="subject_chapters"),
   path('add-lessons/' , views.add_lessons , name="add_lessons"),
   path('lessons/' , views.lessons, name="lessons"),
   path('packages/' , views.course_packages, name="packages"),
   path('add-package/' , views.add_package , name="add_package"),
   path('add-subjects-package/<uid>/' , views.add_subjects_courses,name="add_subjects_courses"),

   path('course-tree/<course_package_uid>/' , views.course_tree , name="course_tree"),
   path('update-lesson/<uid>/' , views.update_lesson ,name="update_lesson"),
   path('course-package-edit/<uid>/' , views.course_package_edit , name="course_package_edit" ),
   path('delete_subject/', views.delete_subject , name="delete_subject"),
   path('delete_chapter/', views.delete_chapter , name="delete_chapter"),
   path('delete_lesson/', views.delete_lesson , name="delete_lesson"),
   path('delete_course_package/', views.delete_course_package , name="delete_course_package"),

   path('test/' , views.test , name="test"),
   path('create-test/' , views.create_test , name="create_test"),
   path('create-live/' , views.create_live , name="create_live"),
   
   
]
