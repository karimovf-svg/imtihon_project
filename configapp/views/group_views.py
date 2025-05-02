from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from ..models import *
from ..serializers import *
from django.shortcuts import get_object_or_404
from ..add_permission import *

# Group
class GroupStudentCreateView(APIView):
    permission_classes = [StaffPermission]

    def get(self, request):
        groups = GroupStudent.objects.all()
        serializer = GroupStudentSerializer(groups, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=GroupStudentSerializer)
    def post(self, request):
        serializer = GroupStudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupStudentDetailView(APIView):
    permission_classes = [TeacherPermission]

    def get_object(self, pk):
        return get_object_or_404(GroupStudent, pk=pk)

    @swagger_auto_schema(request_body=GroupStudentSerializer)
    def put(self, request, pk):
        group = self.get_object(pk)
        serializer = GroupStudentSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Groupni Statudsini o'zgartirish
    @swagger_auto_schema(request_body=GroupStudentUpdateSerializer)
    def patch(self, request, pk):
        group = self.get_object(pk)
        is_active_value = request.data.get('is_active')

        if is_active_value is None:
            return Response(
                {"is_active": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        group.is_active = is_active_value
        group.save()
        serializer = GroupStudentSerializer(group)
        return Response(serializer.data)


    def delete(self, request, pk):
        group = self.get_object(pk)
        group.delete()
        return Response({"detail": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# Teacher o'z groupini studentlarini ko'rishi
class TeacherGetStudent(APIView):
    permission_classes = [TeacherPermission]

    def get_object(self, pk):
        return get_object_or_404(GroupStudent, pk=pk)

    def get(self, request, pk):
        group = self.get_object(pk)
        serializer = GroupStudentSerializer(group)
        return Response(serializer.data)




# Table
class TableCreateView(APIView):
    permission_classes = [StaffPermission]

    def get(self, request):
        table = Table.objects.all()
        serializer = TableSerializer(table, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=TableSerializer)
    def post(self, request):
        serializer = TableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TableDetailView(APIView):
    permission_classes = [StaffPermission]

    def get_object(self, pk):
        return get_object_or_404(Table, pk=pk)

    def get(self, request, pk):
        table = self.get_object(pk)
        serializer = TableSerializer(table)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=TableSerializer)
    def put(self, request, pk):
        table = self.get_object(pk)
        serializer = TableSerializer(table, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        table = self.get_object(pk)
        table.delete()
        return Response({"detail": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



# Table Type
class TableTypeCreateView(APIView):
    permission_classes = [StaffPermission]

    def get(self, request):
        table_type = TableType.objects.all()
        serializer = TableTypeSerializer(table_type, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=TableTypeSerializer)
    def post(self, request):
        serializer = TableTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TableTypeDetailView(APIView):
    permission_classes = [StaffPermission]

    def get_object(self, pk):
        return get_object_or_404(TableType, pk=pk)

    def get(self, request, pk):
        table_type = self.get_object(pk)
        serializer = TableTypeSerializer(table_type)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=TableTypeSerializer)
    def put(self, request, pk):
        table_type = self.get_object(pk)
        serializer = TableTypeSerializer(table_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        table_type = self.get_object(pk)
        table_type.delete()
        return Response({"detail": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# Rooms
class RoomsCreateView(APIView):
    permission_classes = [StaffPermission]

    def get(self, request):
        rooms = Rooms.objects.all()
        serializer = RoomsSerializer(rooms, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=RoomsSerializer)
    def post(self, request):
        serializer = RoomsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoomsDetailView(APIView):
    permission_classes = [StaffPermission]

    def get_object(self, pk):
        return get_object_or_404(Rooms, pk=pk)

    def get(self, request, pk):
        rooms = self.get_object(pk)
        serializer = RoomsSerializer(rooms)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=RoomsSerializer)
    def put(self, request, pk):
        rooms = self.get_object(pk)
        serializer = RoomsSerializer(rooms, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        rooms = self.get_object(pk)
        rooms.delete()
        return Response({"detail": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
