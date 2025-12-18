from rest_framework import serializers
from .models import user_jwtservices

class UserJWTSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_jwtservices
        fields = '__all__'
       