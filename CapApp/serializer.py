from rest_framework import serializers
from .models import Publication

class Serializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
