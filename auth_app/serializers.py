from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import password_validation
from rest_framework import serializers
from .models import CustomUser



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    profile_picture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password', 'role', 'nid',
            'medical_details', 'vaccination_history', 'specialization',
            'contact', 'profile_picture'
        ]

    def validate(self, attrs):
        role = attrs.get('role', 'PATIENT')
        nid = attrs.get('nid', None)

        if role == 'PATIENT' and not nid:
            raise serializers.ValidationError({"nid": "NID is required for patients."})
        return attrs

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'role', 'nid', 'medical_details',
            'vaccination_history', 'specialization', 'contact', 'profile_picture'
        ]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value
