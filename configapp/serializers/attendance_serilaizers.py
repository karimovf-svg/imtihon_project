from rest_framework import serializers
from ..models import Attendance, Status, Student, GroupStudent, Lesson

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'title']

    def to_representation(self, instance):
        # Faqat 'keldi' va 'sababli' statuslarini ko'rsatamiz
        if instance.title.lower() in ['keldi', 'sababli']:
            return super().to_representation(instance)
        return None

class AttendanceSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(queryset=GroupStudent.objects.all(), slug_field='title')
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    lesson = serializers.SlugRelatedField(queryset=Lesson.objects.all(), slug_field='title')
    is_status = serializers.SlugRelatedField(queryset=Status.objects.all(), slug_field='title')

    class Meta:
        model = Attendance
        fields = '__all__'

class AttendancePostSerializer(serializers.Serializer):
    group = serializers.IntegerField()
    lesson = serializers.IntegerField()
    statuses = serializers.DictField(
        child=serializers.ListField(child=serializers.IntegerField()),
        required=False,
        default={}
    )

    def validate(self, data):
        allowed_statuses = {'keldi', 'sababli'}
        for status_title in data.get('statuses', {}).keys():
            if status_title.lower() not in allowed_statuses:
                raise serializers.ValidationError(
                    f"Faqat {', '.join(allowed_statuses)} statuslari ruxsat etilgan"
                )
        return data


class AttendanceUpdateSerializer(serializers.ModelSerializer):
    is_status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all())

    class Meta:
        model = Attendance
        fields = ['group', 'lesson', 'is_status']

