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
   path('preview-video/<uid>/' , views.preview_video, name="preview_video"),
   path('preview-live/<uid>/' , views.preview_video_live, name="preview_video_live"),
   
   path('course-tree/<course_package_uid>/' , views.course_tree , name="course_tree"),
   path('update-lesson/<uid>/' , views.update_lesson ,name="update_lesson"),
   path('course-package-edit/<uid>/' , views.course_package_edit , name="course_package_edit" ),
   path('delete_subject/', views.delete_subject , name="delete_subject"),
   path('delete_chapter/', views.delete_chapter , name="delete_chapter"),
   path('delete_lesson/', views.delete_lesson , name="delete_lesson"),
   path('delete_course_package/', views.delete_course_package , name="delete_course_package"),
   path('allcoupons/' , views.all_coupons, name="coupons"),
   path('addcoupons/' , views.add_coupons, name="addcoupons"),
   path('editcoupon/<uid>/' , views.edit_coupon, name="editcoupon"),
   path('delete_coupon/', views.delete_coupon , name="delete_coupon"),
   path('test/' , views.test , name="test"),
   path('create-test/' , views.create_test , name="create_test"),
   path('create-live/' , views.create_live , name="create_live"),

   #  test urls start
   path('all-test/' , views.all_test , name="all_test"),
   path('add-test/' , views.add_test , name="add_test"),
   path('edit-test/<uid>/' , views.edit_test , name="edit_test"),
   #path('delete-test/<uid>/' , views.delete_test , name="delete_test"),
   path('all-question', views.all_question, name="all_question"),
   path('add-question/' , views.add_question , name="add_question"),

   path('go-live/' , views.go_live  , name="go_live"),
   path('add-live/' , views.add_live , name="add_live"),
   path('edit-live/<uid>/' , views.edit_live  , name="edit_live"),
   path('change_live_status/<uid>/' , views.change_live_status , name="change_live_status"),
   path('package_end_purchase/<uid>/' , views.package_end_purchase , name="package_end_purchase")  ,

   # for manage app
   path('send_notification', views.send_notification, name="send_notification"),
   path('all_slider', views.all_slider, name="all_slider"),
   path('delete_slider/', views.delete_slider , name="delete_slider"),
   path('chat-live/<room_id>/' , views.chat_live, name="chat_live"),

   path('delete_package_lesson/' , views.delete_package_lesson , name="delete_package_lesson"),
   path('remove_coupon/'  , views.remove_coupon, name="remove_coupon")

   
]
