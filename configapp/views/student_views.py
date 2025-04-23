from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from ..serializers import *
from ..add_pagination import *
from ..add_permission import *

class StudentCreateApi(APIView):
    def get(self, request):
        data = {'success': True}
        student = Student.objects.all()
        paginator = CustomPagination()
        paginator.page_size = 2 # Sahifadagi obyektlar soni
        result_page = paginator.paginate_queryset(student, request)
        serializer = StudentSerializer(result_page, many=True)
        data['student'] = serializer.data
        return paginator.get_paginated_response(data=data)

    @swagger_auto_schema(request_body=StudentPostSerializer)
    def post(self, request):
        serializer = StudentPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors)

class StudentUpdateView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Student, pk=pk)

    @swagger_auto_schema(request_body=StudentSerializer)
    def put(self, request, pk):
        student = self.get_object(pk)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            password = serializer.validated_data.get('password')
            serializer.validated_data['password'] = make_password(password)
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
        if serializer.is_valid(raise_exception=True):
            password = serializer.validated_data.get('password')
            serializer.validated_data['password'] = make_password(password)
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
        if serializer.is_valid(raise_exception=True):
            password = serializer.validated_data.get('password')
            serializer.validated_data['password'] = make_password(password)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        parent = self.get_object(pk)
        parent.delete()
        return Response({"detail": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
