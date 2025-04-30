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

# Status
class StatusCreateAPI(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request):
        status = Status.objects.all()
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(status, request)
        serializer = StatusSerializer(status, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(request_body=StatusSerializer)
    def post(self, request):
        serializer = StatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatusDetailAPI(APIView):
    # permission_classes = [IsAdminUser]

    def get_object(self, pk):
        return get_object_or_404(Status, pk=pk)

    @swagger_auto_schema(request_body=StatusSerializer)
    def put(self, request, pk):
        status_obj = self.get_object(pk)
        serializer = StatusSerializer(status_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        status_obj = self.get_object(pk)
        status_obj.delete()
        return Response({'status': True, 'detail': 'Status muaffaqiyatli uchirildi'}, status=status.HTTP_204_NO_CONTENT)


# Attendance
class AttendanceCreateAPI(APIView):
    def get(self, request):
        attendances = Attendance.objects.all()
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(attendances, request)
        serializer = AttendanceSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
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

        # Status obyektlarini olish
        try:
            came_status = Status.objects.get(title__iexact='keldi')
            excused_status = Status.objects.get(title__iexact='sababli')
            absent_status = Status.objects.get(title__iexact='kelmadi')
        except Status.DoesNotExist as e:
            return Response(
                {"error": f"Kerakli status topilmadi: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Guruhdagi barcha talabalar
        students = Student.objects.filter(group__id=group_id)
        marked_students = set()

        # Keldi va sababli studentlarga status belgilash
        for status_title, student_ids in statuses.items():
            status_obj = came_status if status_title.lower() == 'keldi' else excused_status

            for student_id in student_ids:
                marked_students.add(student_id)
                Attendance.objects.update_or_create(
                    group_id=group_id,
                    student_id=student_id,
                    lesson_id=lesson_id,
                    defaults={'is_status': status_obj}
                )

        # Qolganlarga 'kelmadi' belgilash
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


class AttendanceDetailAPI(APIView):
    # permission_classes = [TeacherPermission]

    def get_object(self, pk):
        return get_object_or_404(Attendance, pk=pk)

    @swagger_auto_schema(request_body=AttendanceSerializer)
    def put(self, request, pk):
        # Davomatni yangilash
        attendance = self.get_object(pk)
        serializer = AttendanceSerializer(attendance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Davomat yozuvini o‘chirish
        attendance = self.get_object(pk)
        attendance.delete()
        return Response({'status': True, 'detail': 'Davomat muvaffaqiyatli o‘chirildi'}, status=status.HTTP_204_NO_CONTENT)
