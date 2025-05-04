from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from ..models import *
from ..serializers import LessonSerializer
from django.shortcuts import get_object_or_404
from ..add_permission import *

# Lesson
class LessonCreateView(APIView):
    permission_classes = [TeacherPermission]

    def get(self, request):
        lesson = Lesson.objects.all()
        serializer = LessonSerializer(lesson, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=LessonSerializer)
    def post(self, request):
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LessonDetailView(APIView):
    permission_classes = [TeacherPermission]

    def get_object(self, pk):
        return get_object_or_404(Lesson, pk=pk)

    @swagger_auto_schema(request_body=LessonSerializer)
    def put(self, request, pk):
        lesson = self.get_object(pk)
        serializer = LessonSerializer(lesson, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        lesson = self.get_object(pk)
        lesson.delete()
        return Response({"detail": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)