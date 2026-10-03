from rest_framework import serializers

from .models import RefBook

class RefBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefBook
        fields = (
            "id",
            "code",
            "name",
        )