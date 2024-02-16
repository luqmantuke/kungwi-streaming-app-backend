from rest_framework import serializers
from .models import *

class VifurushiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vifurushi
        fields = '__all__'



