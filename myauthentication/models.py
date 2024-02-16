from django.db import models
from django.contrib.auth.models import AbstractUser, User



class CustomUser(AbstractUser):
    credits = models.PositiveIntegerField(default=0)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    @property
    def get_credits(self):
        return self.credits



class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp_value = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

