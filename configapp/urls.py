from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('auth/post_send_otp/', PhoneSendOTP.as_view()),
    path('auth/post_v_otp/', VerifySMS.as_view()),
    path('users/register/', RegisterUserApi.as_view()),
    path('auth/login/', LoginApi.as_view(), name='token_obtain_pair'),
    path('users/detail/<int:pk>/', UserDetailView.as_view(), name='users_detail'),
    path('users/teacher/create/', TeacherCreateApi.as_view(), name='teacher-create'),
    path('users/teacher/<int:pk>/', TeacherUpdateView.as_view(), name='teacher-update'),
    path('users/student/create/', StudentCreateApi.as_view(), name='student-create'),
    path('users/student/<int:pk>/', StudentUpdateView.as_view(), name='student-update'),
    path('users/parents/create/', ParentsCreateView.as_view(), name='parents-update'),
    path('users/parents/<int:pk>/', ParentsUpdateView.as_view(), name='parents-update'),
    path('course/group-students/', GroupStudentCreateView.as_view(), name='group_create'),
    path('course/group-students/<int:pk>/', GroupStudentDetailView.as_view(), name='group_detail'),
    path('course/table/', TableCreateView.as_view(), name='table_create'),
    path('course/table/<int:pk>/', TableDetailView.as_view(), name='table_detail'),
    path('course/table-type/', TableTypeCreateView.as_view(), name='table_type_create'),
    path('course/table-type/<int:pk>/', TableTypeDetailView.as_view(), name='table_type_detail'),
    path('course/rooms/', RoomsCreateView.as_view(), name='rooms_create'),
    path('course/rooms/<int:pk>/', RoomsDetailView.as_view(), name='rooms_detail'),
    path('course/day/', DayCreateView.as_view(), name='day_create'),
    path('course/day/<int:pk>/', DayDetailView.as_view(), name='day_detail'),
]