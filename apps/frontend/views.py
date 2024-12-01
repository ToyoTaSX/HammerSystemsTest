from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.authentication.models import UserProfile
from apps.authentication.serializers import PhoneNumberSerializer
from apps.authentication.serializers import VerificationCodeSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


class Login(APIView):
    def get(self, request):
        return render(request, 'frontend/login.html')


class Profile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user.profile
        referals_numbers = [i.number for i in UserProfile.objects.filter(activated_code=user.invite_code)]
        data = {
            'number': user.number,
            'invite_code': user.invite_code,
            'activated_code': user.activated_code,
            'referals': referals_numbers
        }
        return render(request, 'frontend/user_profile.html', context=data)
