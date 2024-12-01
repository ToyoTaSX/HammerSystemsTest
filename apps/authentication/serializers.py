from rest_framework import serializers
from apps.authentication.models import UserProfile
from phonenumber_field.serializerfields import PhoneNumberField

class PhoneNumberSerializer(serializers.Serializer):
    number = PhoneNumberField(region='RU')


class VerificationCodeSerializer(serializers.Serializer):
    number = PhoneNumberField(region='RU')
    code = serializers.CharField(max_length=4)

    def validate(self, data):
        number = data.get('number')
        code = data.get('code')

        try:
            user_profile = UserProfile.objects.get(number=number)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError({"phone_number": "Пользователь с таким номером телефона не найден."})

        if not user_profile.is_code_valid(code):
            raise serializers.ValidationError({"code": "Неверный код или срок его действия истек."})

        return data
