from django.contrib import admin
from django.urls import include, path
from . import views
urlpatterns = [
    path('login/', views.Login.as_view()),
    path('', views.Profile.as_view()),
]