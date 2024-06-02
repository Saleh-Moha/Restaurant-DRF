# your_app_name/serializers.py

from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from .models import CustomUser,user_profile

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'date_of_birth', 'national_id', 'password','profile_photo')
        def validate(self, data):
            if not data.get('email'):
                raise serializers.ValidationError({'email': 'This field is required.'})
            if not data.get('first_name'):
                raise serializers.ValidationError({'first_name': 'This field is required.'})
            if not data.get('last_name'):
                raise serializers.ValidationError({'last_name': 'This field is required.'})
            if not data.get('date_of_birth'):
                raise serializers.ValidationError({'date_of_birth': 'This field is required.'})
            if not data.get('national_id'):
                raise serializers.ValidationError({'national_id': 'This field is required.'})
            return data
    
class CustomUserSerializer(UserSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'date_of_birth', 'national_id','profile_photo')


class UserSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = CustomUser
        fields = ['user']