from rest_framework import serializers
from . import UserSerializer
from ..models import *

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'user', 'group', 'is_line', 'descriptions']


class StudentUserSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)
    is_teacher = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_admin = serializers.BooleanField(read_only=True)
    is_student = serializers.BooleanField(read_only=True)
    class Meta:
        model = User
        fields = (
            'id', 'phone_number', 'password', 'email', 'is_active', 'is_staff', 'is_admin', 'is_teacher', 'is_student')


class StudentPostSerializer(serializers.Serializer):
    user = StudentUserSerializer()
    # student = StudentSerializer()
    group = serializers.PrimaryKeyRelatedField(queryset=GroupStudent.objects.all(), many=True)

    class Meta:
        model = Student
        fields = ["id", "user", "group", "is_line", "descriptions"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        user_db = validated_data.pop("user")
        group_db = validated_data.pop("group")
        user_db["is_active"] = True
        user_db["is_student"] = True
        user = User.objects.create_user(**user_db)
        student = Student.objects.create(user=user, **validated_data)
        student.group.set(group_db)
        return student


class ParentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parents
        fields = ['id', 'student', 'full_name', 'phone_number', 'address', 'descriptions']