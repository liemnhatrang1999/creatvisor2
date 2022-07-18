
from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
User= get_user_model()

# class ClientSerializer(serializers.ModelSerializer) :
#     class Meta : 
#         model = Client
#         fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = ('name','email','is_consultant')