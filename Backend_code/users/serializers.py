from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'role', 'phone', 'address')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            role='MEMBER',
            phone=validated_data.get('phone', ''),
            address=validated_data.get('address', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
