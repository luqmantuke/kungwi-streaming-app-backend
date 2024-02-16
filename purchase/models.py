from django.db import models
from myauthentication.models import CustomUser
from kungwi import settings


class MonetizationOn(models.Model):
    monetization_on = models.BooleanField(default=False)


class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    story_type = models.CharField(choices=[('Audio', 'AudioStory'), ('Article', 'ArticleStory')], max_length=10)
    story_id = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_success = models.BooleanField(default=False)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0.0)

    def __str__(self):
        return f"{self.user.username} - {self.story_type} {self.story_id} - {self.timestamp}"


class BuyCredits(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_success = models.BooleanField(default=False)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0.0)


    def __str__(self):
        return self.user.username

class Vifurushi(models.Model):
    title = models.CharField(max_length=1000 )
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    token_amount = models.IntegerField()

    def __str__(self):
        return self.title