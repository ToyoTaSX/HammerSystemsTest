from django.contrib import admin
from django.urls import include, path
from . import views
urlpatterns = [
    path('send-code/', views.SendVerificationCodeView.as_view(), name='auth_send_code'),
    path('verification-code/', views.VerifyCodeView.as_view(), name='auth_verify_code'),
]