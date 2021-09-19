from django.urls import path , include
from . import views_api as views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('document', views.DocumentUpload, )

urlpatterns = [
   path('', views.CoursesView.as_view()), 
   path('subjects/' , views.SubjectsView.as_view()),
   path('get-chapters/' , views.ChaptersView.as_view()),
   path('lessons/' , views.LessonsView.as_view()),
   path('course-packages/' , views.CoursePackageAPI.as_view()),
   path('save-course-package/' , views.SaveCoursePackage.as_view()),
   path('course-package-info/' , views.CoursePackageSubjectsAPI.as_view()),
   path('go-live/' , views.GoLiveView.as_view()),
]

urlpatterns += router.urls