from django.db import models
from myauthentication.models import CustomUser
from purchase.models import  Purchase


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    purchased_stories = models.ManyToManyField(Purchase, blank=True)

    def __str__(self):
        return self.user.username



    def has_purchased_story(self, story_type, story_id):
        return self.purchased_stories.filter(story_type=story_type, story_id=story_id,is_success=True).exists()


