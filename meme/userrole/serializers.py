from rest_framework import serializers
from userrole.models import *

# class TestUserSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = "__all__"


class MemeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemeUser
        fields = "__all__"



