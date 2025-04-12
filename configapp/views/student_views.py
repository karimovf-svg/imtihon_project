from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
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

        # User ni serialize qilish
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.is_student = True
            user_serializer.is_active = True
            user_serializer.password = (make_password(user_serializer.validated_data.get('password')))
            user = user_serializer.save()  # YANGI USER YARATILADI

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