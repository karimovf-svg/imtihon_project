from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from ..serializers import *
from ..add_pagination import *
from ..add_permission import *

class TeacherCreateApi(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request):
        data = {'success': True}
        teachers = Teacher.objects.all()
        paginator = CustomPagination()
        paginator.page_size = 10 # Sahifadagi obyektlar soni
        result_page = paginator.paginate_queryset(teachers, request)
        serializer = TeacherSerializer(result_page, many=True)
        data['teacher'] = serializer.data
        return paginator.get_paginated_response(data=data)

    @swagger_auto_schema(request_body=TeacherPostSerializer)
    def post(self, request):
        serializer = TeacherPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors)

class TeacherUpdateView(APIView):
    # permission_classes = [IsAdminUser, TeacherPermission]

    def get_object(self, pk):
        return get_object_or_404(Teacher, pk=pk)

    @swagger_auto_schema(request_body=TeacherSerializer)
    def put(self, request, pk):
        teacher = self.get_object(pk)
        serializer = TeacherSerializer(teacher, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            password = serializer.validated_data.get('password')
            serializer.validated_data['password'] = make_password(password)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=GroupTeacherUpdateSerializer)
    def patch(self, request, pk=None):
        """
        Teacher o‘ziga tegishli GroupStudent nomini yangilaydi
        """
        teacher = get_object_or_404(Teacher, user=request.user)
        try:
            group = GroupStudent.objects.get(pk=pk, teacher=teacher)
        except GroupStudent.DoesNotExist:
            return Response({
                "status": False,
                "message": "Bunday guruh sizga biriktirilmagan yoki mavjud emas"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = GroupTeacherUpdateSerializer(group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Guruh nomi yangilandi",
                "group": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "status": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class CourseCreateView(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request):
        course = Course.objects.all()
        serializer = CourseSerializer(course, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CourseSerializer)
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseDetailView(APIView):
    # permission_classes = [IsAdminUser]

    def get_object(self, pk):
        return get_object_or_404(Course, pk=pk)

    def get(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CourseSerializer)
    def put(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = self.get_object(pk)
        course.delete()
        return Response({"detail": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class DepartmentCreateView(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request):
        dep = Department.objects.all()
        serializer = DepartmentSerializer(dep, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=DepartmentSerializer)
    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DepartmentDetailView(APIView):
    # permission_classes = [IsAdminUser]

    def get_object(self, pk):
        return get_object_or_404(Department, pk=pk)

    def get(self, request, pk):
        dep = self.get_object(pk)
        serializer = DepartmentSerializer(dep)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=DepartmentSerializer)
    def put(self, request, pk):
        dep = self.get_object(pk)
        serializer = DepartmentSerializer(dep, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        dep = self.get_object(pk)
        dep.delete()
        return Response({"detail": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
