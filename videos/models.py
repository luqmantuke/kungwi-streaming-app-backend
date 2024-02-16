from django.db import models


class Videos(models.Model):
    video_title = models.CharField(max_length=1000)
    video_image = models.ImageField(upload_to='videos/images')
    video_url = models.TextField()
    is_trending = models.BooleanField(default=False)
    video_description = models.CharField(max_length=1000)

    def __str__(self):
        return self.video_title


class Series(models.Model):
    video_title = models.CharField(max_length=1000)
    series_image = models.ImageField(upload_to='series/images')
    is_trending = models.BooleanField(default=False)
    series_description = models.CharField(max_length=1000)

    def __str__(self):
        return self.video_title


class Episode(models.Model):
    series = models.ForeignKey(Series, related_name='series_episodes', on_delete=models.CASCADE)
    episode_title = models.CharField(max_length=1000)
    episode_image = models.ImageField(upload_to='episodes/images')
    episode_url = models.TextField()
    episode_description = models.CharField(max_length=1000)

    def __str__(self):
        return self.episode_title
