from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from ..serializers import *

class TeacherCreateApi(APIView):
    def get(self, request):
        data = {'success': True}
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        data['teacher'] = serializer.data
        return Response(data=data)

    @swagger_auto_schema(request_body=TeacherPostSerializer)
    def post(self, request):
        data = {'success': True}
        user = request.data['user']
        teacher = request.data['teacher']
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
    def get_object(self, pk):
        return get_object_or_404(Teacher, pk=pk)

    @swagger_auto_schema(request_body=TeacherSerializer)
    def put(self, request, pk):
        teacher = self.get_object(pk)
        serializer = TeacherSerializer(teacher, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



        # serializer = TeacherSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     data['data'] = serializer.data
        #     return Response({"status": True, "detail": "Teacher created"})
        # return Response({"status": False, "errors": serializer.errors}, status=400)
        # return Response(data={"status": True},  status=200)