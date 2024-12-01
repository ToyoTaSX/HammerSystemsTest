import random
import string

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now, timedelta
from phonenumber_field.modelfields import PhoneNumberField


def generate_unique_invite_code():
    while True:
        characters = string.ascii_letters + string.digits
        code = ''.join(random.choice(characters) for _ in range(6))
        if not UserProfile.objects.filter(invite_code=code).exists():
            return code

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True)
    number = PhoneNumberField(unique=True, primary_key=True)
    verification_code = models.CharField(max_length=4, blank=True, null=True)
    code_sent_at = models.DateTimeField(blank=True, null=True)

    invite_code = models.CharField(max_length=6, default=generate_unique_invite_code)
    activated_code = models.CharField(max_length=6, blank=True, null=True)


    def generate_verification_code(self):
        self.verification_code = f"{random.randint(1000, 9999)}"
        self.code_sent_at = now()
        self.save()

    def is_code_valid(self, code):
        return (
                self.verification_code == code and
                self.code_sent_at and
                now() <= self.code_sent_at + timedelta(minutes=5)
        )
