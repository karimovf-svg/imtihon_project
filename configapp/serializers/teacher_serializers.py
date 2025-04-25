from rest_framework import serializers
from . import UserSerializer
from ..models import *

class GroupTeacherUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupStudent
        fields = ['id', 'title']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'descriptions']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'title', 'is_active', 'search_fields', 'descriptions']

class TeacherSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Teacher
        fields = ['id', 'user', 'department', 'course', 'descriptions']


class TeacherUserSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)
    is_teacher = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_admin = serializers.BooleanField(read_only=True)
    is_student = serializers.BooleanField(read_only=True)
    class Meta:
        model = User
        fields = (
            'id', 'phone_number', 'password', 'email', 'is_active', 'is_staff', 'is_admin', 'is_teacher', 'is_student')

class TeacherPostSerializer(serializers.Serializer):
    user = TeacherUserSerializer()
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), many=True)
    descriptions = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'department', 'course', 'descriptions']
        read_only_fields = ["user"]

    def create(self, validated_data):
        user_db = validated_data.pop("user")
        course_db = validated_data.pop("course")
        user_db["is_active"] = True
        user_db["is_teacher"] = True
        user = User.objects.create_user(**user_db)
        teacher = Teacher.objects.create(user=user, **validated_data)
        teacher.course.set(course_db)
        return teacher