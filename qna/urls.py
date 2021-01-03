from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('new/', views.newQuestion, name="newQuestion"),
    path('about/', views.about, name="about"),
    path('register/', views.register, name="register"),
    path('myQuestions/', views.myQuestions, name="myQuestions"),
    path('myAnswers/', views.myAnswers, name="myAnswers"),
    path('updateVote/', views.updateVote, name="updateVote"),
    path('search/', views.search, name="search"),
    path('<slug:slug>/', views.question, name="question")
]
