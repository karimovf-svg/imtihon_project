from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from ..serializers import *
from ..add_pagination import *
from ..add_permission import *

class TeacherCreateApi(APIView):
    permission_classes = [IsAuthenticated, TeacherPermission]

    def get(self, request):
        data = {'success': True}
        teachers = Teacher.objects.all()
        paginator = CustomPagination()
        paginator.page_size = 2 # Sahifadagi obyektlar soni
        result_page = paginator.paginate_queryset(teachers, request)
        serializer = TeacherSerializer(result_page, many=True)
        data['teacher'] = serializer.data
        return paginator.get_paginated_response(data=data)

    @swagger_auto_schema(request_body=TeacherPostSerializer)
    def post(self, request):
        data = {'success': True}
        user = request.data['user']
        teacher = request.data['teacher']
        phone_number = user['phone_number']
        user_serializer = UserSerializer(data=user)
        user['is_teacher'] = True
        user['is_active'] = True

        # User ni serialize qilish
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.password = (make_password(user_serializer.validated_data.get('password')))
            user = user_serializer.save()  # YANGI USER YARATILADI
            # Userni ID sini olish
            user_id = User.objects.filter(phone_number=phone_number).values('id')[0]['id']
            teacher['user'] = user_id   # Teacher uchun user_id biriktiramiz
            teacher_serializer = TeacherSerializer(data=teacher)
            if teacher_serializer.is_valid(raise_exception=True):
                teacher_serializer.save()
                data['user'] = user_serializer.data
                data['teacher'] = teacher_serializer.data
                return Response(data=data)
            return Response(data=teacher_serializer.errors)
        return Response(data=user_serializer.errors)

class TeacherUpdateView(APIView):
    permission_classes = [IsAuthenticated, TeacherPermission]
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
