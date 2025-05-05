from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import *
from ..serializers import *
from ..add_permission import *
from ..add_pagination import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Attendance
class AttendanceCreateAPI(APIView):
    permission_classes = [TeacherPermission]

    def get(self, request):
        attendances = Attendance.objects.all()
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(attendances, request)
        serializer = AttendanceSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'group': openapi.Schema(type=openapi.TYPE_INTEGER, description='Guruh ID'),
                'lesson': openapi.Schema(type=openapi.TYPE_INTEGER, description='Dars ID'),
                'statuses': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="Faqat 'keldi' va 'sababli' statuslari bilan talabalar IDlari",
                    additional_properties=openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_INTEGER)
                    )
                )
            },
            example={
                "group": 0,
                "lesson": 0,
                "statuses": {
                    "keldi": [],
                    "sababli": []
                }
            }
        ),
        responses={
            201: "Davomat muvaffaqiyatli saqlandi",
            400: "Noto'g'ri ma'lumotlar"
        }
    )

    def post(self, request):
        serializer = AttendancePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        group_id = data['group']
        lesson_id = data['lesson']
        statuses = data.get('statuses', {})

        # Statuslarni model enum'idan olish
        came_status = Attendance.StatusChoices.KELDI
        excused_status = Attendance.StatusChoices.SABABLI
        absent_status = Attendance.StatusChoices.KELMADI

        students = Student.objects.filter(group__id=group_id)
        marked_students = set()

        for status_title, student_ids in statuses.items():
            status_obj = None
            if status_title.lower() == 'keldi':
                status_obj = came_status
            elif status_title.lower() == 'sababli':
                status_obj = excused_status

            for student_id in student_ids:
                marked_students.add(student_id)
                Attendance.objects.update_or_create(
                    group_id=group_id,
                    student_id=student_id,
                    lesson_id=lesson_id,
                    defaults={'is_status': status_obj}
                )

        for student in students:
            if student.id not in marked_students:
                Attendance.objects.update_or_create(
                    group_id=group_id,
                    student_id=student.id,
                    lesson_id=lesson_id,
                    defaults={'is_status': absent_status}
                )

        return Response(
            {
                "message": "Davomat muvaffaqiyatli saqlandi",
                "absent_students": list(students.exclude(id__in=marked_students).values_list('id', flat=True))
            },
            status=status.HTTP_201_CREATED
        )


class AttendanceUpdateAPI(APIView):
    permission_classes = [TeacherPermission]

    def get_object(self, student_id, lesson_id, group_id):
        return get_object_or_404(
            Attendance,
            student_id=student_id,
            lesson_id=lesson_id,
            group_id=group_id
        )

    @swagger_auto_schema(request_body=AttendanceUpdateSerializer)
    def put(self, request):
        student_id = request.data.get('student')
        lesson_id = request.data.get('lesson')
        group_id = request.data.get('group')

        if not all([student_id, lesson_id, group_id]):
            return Response({'error': 'student, lesson va group maydonlari talab qilinadi.'},
                            status=status.HTTP_400_BAD_REQUEST)

        attendance = self.get_object(student_id, lesson_id, group_id)
        serializer = AttendanceUpdateSerializer(attendance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(AttendanceSerializer(attendance).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttendanceDetailAPI(APIView):
    permission_classes = [TeacherPermission]

    def get_object(self, pk):
        return get_object_or_404(Attendance, pk=pk)

    def delete(self, request, pk):
        attendance = get_object_or_404(Attendance, pk=pk)
        attendance.delete()
        return Response({'status': True, 'detail': 'Davomat muvaffaqiyatli o‘chirildi'}, status=status.HTTP_204_NO_CONTENT)



