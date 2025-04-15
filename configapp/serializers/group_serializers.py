from rest_framework import serializers
from . import UserSerializer
from ..models import *

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupStudent
        fields = ['id', 'title', 'course', 'teacher', 'table', 'start_date', 'end_date', 'descriptions']


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

class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = ['id', 'title', 'descriptions']
