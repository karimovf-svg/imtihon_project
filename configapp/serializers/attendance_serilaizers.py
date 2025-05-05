from rest_framework import serializers
from ..models import Attendance, Student, GroupStudent, Lesson
from django.shortcuts import get_object_or_404


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


class AttendancePostSerializer(serializers.Serializer):
    group = serializers.IntegerField()
    lesson = serializers.IntegerField()
    statuses = serializers.DictField(
        child=serializers.ListField(
            child=serializers.IntegerField()
        )
    )


class AttendanceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['group', 'lesson', 'student', 'is_status']