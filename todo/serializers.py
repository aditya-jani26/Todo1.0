# serializers.py
from rest_framework import serializers
from .models import Todo , Person

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class ToDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
    
class LogoutSerializer(serializers.Serializer):
    pass