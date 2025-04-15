from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from ..serializers import *

class StudentCreateApi(APIView):
    def get(self, request):
        data = {'success': True}
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)
        data['student'] = serializer.data
        return Response(data=data)

    @swagger_auto_schema(request_body=StudentPostSerializer)
    def post(self, request):
        data = {'success': True}
        user = request.data['user']
        student = request.data['student']
        phone_number = user['phone_number']
        user_serializer = UserSerializer(data=user)
        user['is_student'] = True
        user['is_active'] = True

        # User ni serialize qilish
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.password = (make_password(user_serializer.validated_data.get('password')))
            user = user_serializer.save()  # YANGI USER YARATILADI
            # Userni ID sini olish
            user_id = User.objects.filter(phone_number=phone_number).values('id')[0]['id']
            student['user'] = user_id   # Student uchun user_id biriktiramiz
            student_serializer = StudentSerializer(data=student)
            if student_serializer.is_valid(raise_exception=True):
                student_serializer.save()
                data['user'] = user_serializer.data
                data['student'] = student_serializer.data
                return Response(data=data)
            return Response(data=student_serializer.errors)
        return Response(data=user_serializer.errors)

class StudentUpdateView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Student, pk=pk)

    @swagger_auto_schema(request_body=StudentSerializer)
    def put(self, request, pk):
        student = self.get_object(pk)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ParentsCreateView(APIView):
    def get(self, request):
        parent = Parents.objects.all()
        serializer = ParentsSerializer(parent, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ParentsSerializer)
    def post(self, request):
        serializer = ParentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ParentsUpdateView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Parents, pk=pk)

    @swagger_auto_schema(request_body=ParentsSerializer)
    def put(self, request, pk):
        parent = self.get_object(pk)
        serializer = ParentsSerializer(parent, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        parent = self.get_object(pk)
        parent.delete()
        return Response({"detail": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
