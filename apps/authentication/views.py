from time import sleep

from django.contrib.auth import authenticate, login
from django.middleware import csrf
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings
from apps.authentication.models import UserProfile
from apps.authentication.serializers import PhoneNumberSerializer
from apps.authentication.serializers import VerificationCodeSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


class SendVerificationCodeView(APIView):
    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            number = serializer.validated_data['number']

            user_profile, created = UserProfile.objects.get_or_create(number=number)

            if created and not user_profile.user:
                user = User.objects.create(username=number)
                user_profile.user = user
                user_profile.save()

            user_profile.generate_verification_code()
            sleep(2)
            return Response({
                "message": "Код подтверждения отправлен (заглушка).",
                "code": user_profile.verification_code
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(APIView):
    def post(self, request):
        serializer = VerificationCodeSerializer(data=request.data)
        if serializer.is_valid():
            number = serializer.validated_data['number']

            try:
                user_profile = UserProfile.objects.get(number=number)
            except UserProfile.DoesNotExist:
                return Response({"number": "Пользователь не найден."}, status=status.HTTP_404_NOT_FOUND)

            if not user_profile.user:
                user = User.objects.create(username=number)
                user_profile.user = user
                user_profile.save()
            else:
                user = user_profile.user

            csrf.get_token(request)

            refresh = RefreshToken.for_user(user)
            response = Response()

            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                value=refresh.access_token,
                expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'])

            response.data = {
                "message": "Успешный вход.",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
