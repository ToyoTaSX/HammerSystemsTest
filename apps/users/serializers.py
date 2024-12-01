from rest_framework import serializers

from apps.authentication.models import UserProfile


class InviteCodeSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=6)

    def validate(self, data):
        invite_code = data.get('invite_code')
        if not invite_code.isalnum():
            raise serializers.ValidationError({"invite_Code": "Недопустимые символы"})

        try:
            user_profiles = UserProfile.objects.get(invite_code=invite_code)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError({"invite_Code": "Пользователь с таким кодом не найден."})

        return data
