from rest_framework import serializers
from ..models import *

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'group', 'teacher', 'lesson_date']