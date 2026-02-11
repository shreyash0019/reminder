from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


# 🔹 Register Serializer
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            role=validated_data.get('role', 'patient')  # default role
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# 🔹 Role-Based Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        role = data.get("role")

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid username or password")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")

        if user.role != role:
            raise serializers.ValidationError("Role mismatch")

        data['user'] = user
        return data
