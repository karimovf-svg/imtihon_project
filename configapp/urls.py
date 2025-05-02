from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

# Homework
router = DefaultRouter()
router.register('create',HomeworkViewSet,basename='homework')
router.register('submission',HomeworkSubmissionViewSet,basename='homework-submission')
router.register('review',HomeworkReviewViewSet,basename='homework-review')


urlpatterns = [
    # Auth
    path('auth/post_send_otp/', PhoneSendOTP.as_view()),
    path('auth/post_v_otp/', VerifySMS.as_view()),
    path('auth/login/', LoginApi.as_view(), name='token_obtain_pair'),
    path('auth/new-password/', ChangePasswordView.as_view(), name='password_update'),

    # Attendance
    path('attendance/status-create/', StatusCreateAPI.as_view(), name='status_create'),
    path('attendance/status-detail/<int:pk>/', StatusDetailAPI.as_view(), name='status-detail'),
    path('attendance/create/', AttendanceCreateAPI.as_view(), name='attendance_create'),
    path('attendance/detail/<int:pk>/', AttendanceDetailAPI.as_view(), name='attendance_detail'),


    # Users
    path('users/create/', RegisterUserApi.as_view(), name='users_create'),
    path('users/detail/<int:pk>/', UserDetailView.as_view(), name='users_detail'),
    path('users/admin-create/', CreateAdminUserView.as_view(), name='admin_create'),
    path('users/department/create/', DepartmentCreateView.as_view(), name='department_create'),
    path('users/department/<int:pk>/', DepartmentDetailView.as_view(), name='department_detail'),
    path('users/teacher/create/', TeacherCreateApi.as_view(), name='teacher_create'),
    path('users/teacher/detail/<int:pk>/', TeacherUpdateView.as_view(), name='teacher_update'),
    path('users/student/create/', StudentCreateApi.as_view(), name='student_create'),
    path('users/student/detail/<int:pk>/', StudentUpdateView.as_view(), name='student_update'),
    path('users/parents/create/', ParentsCreateView.as_view(), name='parents_update'),
    path('users/parents/detail/<int:pk>/', ParentsUpdateView.as_view(), name='parents_update'),

    # Course
    path('course/create/', CourseCreateView.as_view(), name='course_create'),
    path('course/detail/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('course/group-students/create/', GroupStudentCreateView.as_view(), name='group_create'),
    path('course/group-students/detail/<int:pk>/', GroupStudentDetailView.as_view(), name='group_detail'),
    path('course/table/create/', TableCreateView.as_view(), name='table_create'),
    path('course/table/detail/<int:pk>/', TableDetailView.as_view(), name='table_detail'),
    path('course/table-type/create/', TableTypeCreateView.as_view(), name='table_type_create'),
    path('course/table-type/detail/<int:pk>/', TableTypeDetailView.as_view(), name='table_type_detail'),
    path('course/rooms/create/', RoomsCreateView.as_view(), name='rooms_create'),
    path('course/rooms/detail/<int:pk>/', RoomsDetailView.as_view(), name='rooms_detail'),
    path('homeworks/', include(router.urls)),
    # path('course/teacher-group-title/update/<int:pk>/', TeacherUpdateGrouptitle.as_view(), name='group_title_update'),

    # Statistics
    path('statistic/attendance-student/<int:student_id>/', StudentAttendanceAPIView.as_view(), name='student_get_attendances'),
    path('statistic/payments-student/<int:student_id>/', StudentPaymentAPIView.as_view(), name='student_get_payment'),
    path('statistic/students/', StudentFilterView.as_view(), name='statistic_students'),
    path('statistic/teachers/', TeacherFilterView.as_view(), name='teachers_statistic'),
    path('statistic/attendance/', AttendanceFilterView.as_view(), name='attendance_statistics'),
    path('statistic/payments/', PaymentFilterView.as_view(), name='payments_statistics'),

    # Payments
    path('payments/months/create/', MonthCreateView.as_view(), name='month_create'),
    path('payments/months/<int:pk>/', MonthDetailView.as_view(), name='month_detail'),
    path('payments/type/create/', PaymentTypeCreateView.as_view(), name='payment_type_create'),
    path('payments/type/<int:pk>/', PaymentTypeDetailView.as_view(), name='payment_type_detail'),
    path('payments/payment-create/', PaymentCreateView.as_view(), name='payment_create'),
    path('payments/payment/<int:pk>/', PaymentDetailView.as_view(), name='payment_detail'),
]