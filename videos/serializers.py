from .models import *
from rest_framework import serializers


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videos
        fields = "__all__"


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = '__all__'


class SeriesSerializer(serializers.ModelSerializer):
    series_episodes = EpisodeSerializer(many=True, read_only=True)

    class Meta:
        model = Series
        fields = '__all__'
