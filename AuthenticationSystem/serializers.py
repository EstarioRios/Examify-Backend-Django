from rest_framework import serializers
from .models import CustomUser


class CustomUserFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "user_name",
            "user_type",
            "active_mode",
        ]


class CustomUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["user_name", "user_type"]
