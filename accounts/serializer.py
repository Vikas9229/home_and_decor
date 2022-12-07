from csv import field_size_limit
from rest_framework import serializers
from django.contrib.auth import authenticate
from employee.models import CustomUser as User
class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'