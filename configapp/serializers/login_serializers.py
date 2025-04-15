from django.contrib.auth import authenticate
from rest_framework import serializers
from ..models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'phone_number', 'password', 'email', 'is_active', 'is_staff', 'is_admin', 'is_teacher', 'is_student')


# class ChangePasswordSerializer(serializers.Serializer):
#     old_password = serializers.CharField(required=True, write_only=True)
#     new_password = serializers.CharField(required=True, write_only=True)
#     re_new_password = serializers.CharField(required=True, write_only=True)
#
#     def update(self, instance, validated_data):
#
#         instance.password = validated_data.get('password', instance.password)
#         if not validated_data['old_password']:
#             raise serializers.ValidationError({'old_password': 'not found'})
#         if not validated_data['new_password']:
#             raise serializers.ValidationError({'new_password': 'not found'})

class VerifySMSSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    verification_code = serializers.CharField()

class SMSSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()  # username o'rniga phone
    password = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        password = attrs.get("password")

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "success": False,
                "message": "User does not exist"
            })

        auth_user = authenticate(phone_number=phone_number, password=password)
        if auth_user is None:
            raise serializers.ValidationError({
                "success": False,
                "message": "Phone or password is invalid"
            })

        attrs['user'] = auth_user
        return attrs

