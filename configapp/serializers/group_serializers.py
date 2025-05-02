from rest_framework import serializers
from . import UserSerializer
from ..models import *

class StudentSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='user.phone_number')

    class Meta:
        model = Student
        fields = ['id', 'phone_number', 'is_active', 'descriptions']


class GroupStudentSerializer(serializers.ModelSerializer):
    students = serializers.SerializerMethodField()

    class Meta:
        model = GroupStudent
        fields = ['id', 'title', 'course', 'teacher', 'table', 'is_active', 'start_date', 'end_date', 'descriptions', 'students']

    def get_students(self, obj):
        students = Student.objects.filter(group=obj)
        return StudentSerializer(students, many=True).data

# class GroupStudentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GroupStudent
#         fields = ['id', 'title', 'course', 'teacher', 'table', 'is_active', 'start_date', 'end_date', 'descriptions']

class GroupStudentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupStudent
        fields = ['id', 'is_active']


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'start_time', 'end_time', 'room', 'type', 'descriptions']

class TableTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableType
        fields = ['id', 'title', 'descriptions']

class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = ['id', 'title', 'descriptions']

