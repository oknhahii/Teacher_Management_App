from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('teacher_infor/<str:pk>/', views.teacherInfo, name="teacher-info"),

    path('create-teacher/', views.createTeacher, name="create-teacher"),
    path('update-teacher/<int:pk>/', views.updateTeacher, name="update-teacher"),
    path('delete-teacher/<int:pk>/', views.deleteTeacher, name="delete-teacher"),
    path('add-class/<int:pk>/',views.addClass, name="add-class")
]