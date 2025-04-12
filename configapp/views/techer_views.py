from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
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

        # User ni serialize qilish
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.is_teacher = True
            user_serializer.is_active = True
            user_serializer.password = (make_password(user_serializer.validated_data.get('password')))
            user = user_serializer.save()  # YANGI USER YARATILADI

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

        # serializer = TeacherSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     data['data'] = serializer.data
        #     return Response({"status": True, "detail": "Teacher created"})
        # return Response({"status": False, "errors": serializer.errors}, status=400)
        # return Response(data={"status": True},  status=200)