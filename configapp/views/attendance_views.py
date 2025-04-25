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
    # permission_classes = [TeacherPermission]

    # def get(self, request):
    #     attendances = Attendance.objects.all()
    #     paginator = CustomPagination()
    #     result_page = paginator.paginate_queryset(attendances, request)
    #     serializer = AttendanceSerializer(result_page, many=True)
    #     return paginator.get_paginated_response(serializer.data)
    #
    # @swagger_auto_schema(request_body=AttendanceSerializer)
    # def post(self, request):
    #     serializer = AttendanceSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        attendances = Attendance.objects.all()
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(attendances, request)
        serializer = AttendanceSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'group': openapi.Schema(type=openapi.TYPE_INTEGER),
            'status': openapi.Schema(type=openapi.TYPE_INTEGER),
            'students': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_INTEGER)
            ),
        },
        required=['group', 'status', 'students']
    ))
    def post(self, request):
        group = request.data.get('group')
        status_id = request.data.get('status')
        students = request.data.get('students')

        if not all([group, status_id, students]):
            return Response({"detail": "All fields (group, status, students) are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(students, list):
            return Response({"students": "This field must be a list of student IDs."},
                            status=status.HTTP_400_BAD_REQUEST)

        created_attendances = []

        for student_id in students:
            data = {
                'group': group,
                'status': status_id,
                'student': student_id
            }
            serializer = AttendanceSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                created_attendances.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "detail": f"{len(created_attendances)} ta davomat muvaffaqiyatli yaratildi.",
            "data": created_attendances
        }, status=status.HTTP_201_CREATED)


class AttendanceDetailAPI(APIView):
    # permission_classes = [TeacherPermission]

    def get_object(self, pk):
        return get_object_or_404(Attendance, pk=pk)

    def get(self, request, pk):
        attendance = self.get_object(pk)
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=AttendanceSerializer)
    def put(self, request, pk):
        attendance = self.get_object(pk)
        serializer = AttendanceSerializer(attendance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        attendance = self.get_object(pk)
        attendance.delete()
        return Response({'status': True, 'detail': 'Attendance muaffaqiyatli uchirildi'}, status=status.HTTP_204_NO_CONTENT)

