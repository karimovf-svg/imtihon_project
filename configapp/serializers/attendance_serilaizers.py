from rest_framework import serializers
from ..models import Attendance, Status, Student

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
    group = serializers.PrimaryKeyRelatedField(read_only=True)
    student = serializers.PrimaryKeyRelatedField(read_only=True)
    lesson = serializers.PrimaryKeyRelatedField(read_only=True)
    is_status = serializers.StringRelatedField()  # yoki kerakli serializer

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




# from rest_framework import serializers
# from ..models import Attendance, Status
#
# class StatusSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Status
#         fields = '__all__'
#
# class AttendanceSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Attendance
#         fields = '__all__'
#
# class AttendancePostSerializer(serializers.Serializer):
#     group = serializers.IntegerField()
#     lesson = serializers.IntegerField()
#     statuses = serializers.DictField(
#         child=serializers.ListField(
#             child=serializers.IntegerField()
#         )
#     )
