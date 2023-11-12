from django.urls import path

from . import views

urlpatterns = [
    path('get-subjects/', views.SubjectList.as_view()),
    path('get-lectures/', views.LectureList.as_view()),
    path('get-user-lectures/', views.UserLectureList.as_view()),
    path('get-subject-lectures/', views.SubjectLectureList.as_view()),
    path('upload-voice/', views.upload_voice),
    path('upload-slides/', views.upload_slides),
]