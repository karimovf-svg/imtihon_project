from datetime import datetime
from django.db.models import Count, Q, Sum
from django.utils.timezone import make_aware
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from ..models import *
from ..serializers import *
from ..add_permission import *

# Students Statistics
class StudentFilterView(APIView):
    permission_classes = [StaffPermission]

    @swagger_auto_schema(request_body=DateFilterSerializer)
    def post(self, request):
        serializer = DateFilterSerializer(data=request.data)  # Kiruvchi ma'lumotlarni tekshirish
        if not serializer.is_valid():  # Agar ma'lumotlar noto'g'ri bo'lsa
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Xatolikni qaytarish

        # Sanalarni olish
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']

        # Sanalarni tayyorlash (timezone bilan)
        start_date = make_aware(datetime.combine(start_date, datetime.min.time()))  # Kun boshlanishi (00:00:00)
        end_date = make_aware(datetime.combine(end_date, datetime.max.time()))  # Kun oxiri (23:59:59)

        # Statistik ma'lumotlarni olish
        total_students = Student.objects.count()  # Jami talabalar soni
        graduated_students = Student.objects.filter(group__is_active=False, created_ed__range=[start_date,end_date]).count()  # Bitirgan talabalar
        studying_students = Student.objects.filter(group__is_active=True, created_ed__range=[start_date,end_date]).count()  # O'qiyotgan talabalar
        registered_students = Student.objects.filter(created_ed__range=[start_date, end_date]).count()  # Ro'yxatdan o'tgan talabalar

        # Natijani qaytarish
        return Response({
            "total_students": total_students,
            "registered_students": registered_students,
            "studying_students": studying_students,
            "graduated_students": graduated_students,
        }, status=status.HTTP_200_OK)


# Teachers Statistics
class TeacherFilterView(APIView):
    permission_classes = [StaffPermission]

    @swagger_auto_schema(request_body=DateFilterSerializer)
    def post(self, request):
        serializer = DateFilterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']

        start_date = make_aware(datetime.combine(start_date, datetime.min.time()))
        end_date = make_aware(datetime.combine(end_date, datetime.max.time()))

        total_teachers = Teacher.objects.count()  # Jami o'qituvchilar soni
        registered_teachers = Teacher.objects.filter(
            created_ed__range=[start_date, end_date]).count()  # Ro'yxatdan o'tgan o'qituvchilar

        # Eng ko'p talabaga ega bo'lgan 10 ta o'qituvchi
        top_teachers = (
            Student.objects.filter(created_ed__range=[start_date, end_date])
            .values("group__teacher__user__phone_number")  # O'qituvchining telefon raqami
            .annotate(total_students=Count("id"))  # Har bir o'qituvchining talabalari soni
            .order_by("-total_students")[:10]  # Eng ko'p talabaga ega 10 ta o'qituvchi
        )

        return Response({
            "total_teachers": total_teachers,
            "registered_teachers": registered_teachers,
            "top_teachers": top_teachers,
        }, status=status.HTTP_200_OK)


# Davomat Statistics
class AttendanceFilterView(APIView):
    permission_classes = [StaffPermission]

    @swagger_auto_schema(request_body=DateFilterSerializer)
    def post(self, request):
        serializer = DateFilterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']

        start_date = make_aware(datetime.combine(start_date, datetime.min.time()))
        end_date = make_aware(datetime.combine(end_date, datetime.max.time()))

        # Status IDlarini olish
        try:
            came_status = Status.objects.get(title__iexact='keldi')
            absent_status = Status.objects.get(title__iexact='kelmadi')
            late_status = Status.objects.get(title__iexact='kechikdi')
            excused_status = Status.objects.get(title__iexact='sababli')
        except Status.DoesNotExist as e:
            return Response(
                {"error": f"Status topilmadi: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        attendance_stats = (
            Attendance.objects.filter(created_ed__range=[start_date.date(), end_date.date()])
            .aggregate(
                total_present=Count("id", filter=Q(is_status=came_status)),
                total_absent=Count("id", filter=Q(is_status=absent_status)),
                total_late=Count("id", filter=Q(is_status=late_status)),
                total_excused=Count("id", filter=Q(is_status=excused_status)),
            )
        )
        return Response(attendance_stats, status=status.HTTP_200_OK)


# Payments Statistics
class PaymentFilterView(APIView):
    permission_classes = [StaffPermission]

    @swagger_auto_schema(request_body=DateFilterSerializer)
    def post(self, request):
        serializer = DateFilterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']

        start_date = make_aware(datetime.combine(start_date, datetime.min.time()))
        end_date = make_aware(datetime.combine(end_date, datetime.max.time()))

        # To'lov statistikasi
        payment_stats = (
            Payment.objects.filter(created_ed__range=[start_date, end_date])
            .aggregate(
                total_amount=Sum("price"),  # Jami to'langan summa
                total_students=Count("student", distinct=True)  # To'lov qilgan talabalar soni
            )
        )
        return Response(payment_stats, status=status.HTTP_200_OK)