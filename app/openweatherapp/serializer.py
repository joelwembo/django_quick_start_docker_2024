from rest_framework import serializers

from .models import City


class Citieserializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name")