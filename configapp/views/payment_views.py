from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..add_pagination import *
from ..add_permission import *
from ..models import Payment, Month, PaymentType, Student
from ..serializers import MonthSerializer, PaymentTypeSerializer, PaymentSerializer


#Month
class MonthCreateView(APIView):
    permission_classes = [StaffPermission]

    def get(self, request):
        months = Month.objects.all()
        serializer = MonthSerializer(months, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=MonthSerializer)
    def post(self, request):
        serializer = MonthSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MonthDetailView(APIView):
    permission_classes = [StaffPermission]

    @swagger_auto_schema(request_body=MonthSerializer)
    def put(self, request, pk):
        month = get_object_or_404(Month, pk=pk)
        serializer = MonthSerializer(month, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        month = get_object_or_404(Month, pk=pk)
        month.delete()
        return Response({'status': True, 'detail': 'Month o‘chirildi'}, status=status.HTTP_204_NO_CONTENT)


#PaymentType
class PaymentTypeCreateView(APIView):
    permission_classes = [StaffPermission]

    def get(self, request):
        types = PaymentType.objects.all()
        serializer = PaymentTypeSerializer(types, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=PaymentTypeSerializer)
    def post(self, request):
        serializer = PaymentTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentTypeDetailView(APIView):
    permission_classes = [StaffPermission]

    @swagger_auto_schema(request_body=PaymentTypeSerializer)
    def put(self, request, pk):
        type = get_object_or_404(PaymentType, pk=pk)
        serializer = PaymentTypeSerializer(type, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        type = get_object_or_404(PaymentType, pk=pk)
        type.delete()
        return Response({'status': True, 'detail': 'Payment type o‘chirildi'}, status=status.HTTP_204_NO_CONTENT)


#Payment
class PaymentCreateView(APIView):
    permission_classes = [StaffPermission]

    def get(self, request):
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=PaymentSerializer)
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentDetailView(APIView):
    permission_classes = [StaffPermission]

    def get(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=PaymentSerializer)
    def put(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        serializer = PaymentSerializer(payment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk)
        payment.delete()
        return Response({'status': True, 'detail': 'Payment o‘chirildi'}, status=status.HTTP_204_NO_CONTENT)



# Student o'z to'lo'vlarini ko'rish
class StudentPaymentAPIView(APIView):
    permission_classes = [StudentPermission]

    def get(self, request, student_id):
        student = get_object_or_404(Student, id=student_id)
        payment = Payment.objects.filter(student=student)
        serializer = PaymentSerializer(payment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
