from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.authentication.models import UserProfile
from apps.authentication.serializers import PhoneNumberSerializer
from apps.authentication.serializers import VerificationCodeSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import InviteCodeSerializer


class InviteCode(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = InviteCodeSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['invite_code']
            if request.user.profile.invite_code == code:
                return Response({'message': 'Нельзя применить собственный код'}, status=400)
            if request.user.profile.activated_code is not None:
                return Response({'message': 'Вы уже применяли код'}, status=400)

            request.user.profile.activated_code = code
            request.user.profile.save()
            return Response({'message': 'Код успешно применен'}, status=200)
        return Response({'message': serializer.errors}, status=400)


class Profile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        referals = UserProfile.objects.filter(activated_code=user.profile.invite_code)
        referals_numbers = [str(r.number) for r in referals]
        return Response({
            'your_number': str(user.profile.number),
            'your_code': user.profile.invite_code,
            'activated_code': user.profile.activated_code,
            'referals_numbers': referals_numbers
        }, status=200)
