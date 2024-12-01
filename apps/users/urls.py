from django.contrib import admin
from django.urls import include, path
from . import views
urlpatterns = [
    path('invite-code/', views.InviteCode.as_view()),
    path('profile/', views.Profile.as_view()),
]