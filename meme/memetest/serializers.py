from rest_framework import serializers
from memetest.models import *

# class TestUserSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()

class TestUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestUser
        # fields = ("username", "password")
        fields = "__all__"

class TestStarSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestStar
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class StarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Star
        fields = "__all__"

