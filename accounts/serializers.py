from rest_framework import serializers
from .models import User, LoginHistory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'email_verified', 'last_login', 'last_login_ip']
        read_only_fields = ['email_verified', 'last_login', 'last_login_ip']

class LoginHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginHistory
        fields = ['id', 'timestamp', 'ip_address', 'user_agent', 'status']