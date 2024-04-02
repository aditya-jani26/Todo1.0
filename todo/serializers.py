# serializers.py
from rest_framework import serializers
from .models import Todo

class ToDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id','date' ,'title', 'description', 'completed']

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = Todo
        fields = ('email','password')

class LogoutSerializer(serializers.Serializer):
    pass