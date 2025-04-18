from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    # Auth
    path('auth/post_send_otp/', PhoneSendOTP.as_view()),
    path('auth/post_v_otp/', VerifySMS.as_view()),
    path('auth/login/', LoginApi.as_view(), name='token_obtain_pair'),
    # path('auth/new-password/', ChangePasswordView.as_view(), name='password_update'),

    # Users
    path('users/create/', RegisterUserApi.as_view()),
    path('users/detail/<int:pk>/', UserDetailView.as_view(), name='users_detail'),
    path('users/department/create/', DepartmentCreateView.as_view(), name='department_create'),
    path('users/department/<int:pk>/', DepartmentDetailView.as_view(), name='department_detail'),
    path('users/teacher/create/', TeacherCreateApi.as_view(), name='teacher_create'),
    path('users/teacher/group-update-title/<int:pk>/', TeacherViewPermission.as_view(), name='teacher_permission'),
    path('users/teacher/<int:pk>/', TeacherUpdateView.as_view(), name='teacher_update'),
    path('users/student/create/', StudentCreateApi.as_view(), name='student_create'),
    path('users/student/<int:pk>/', StudentUpdateView.as_view(), name='student_update'),
    path('users/parents/create/', ParentsCreateView.as_view(), name='parents_update'),
    path('users/parents/<int:pk>/', ParentsUpdateView.as_view(), name='parents_update'),

    # Course
    path('course/create/', CourseCreateView.as_view(), name='course_create'),
    path('course/detail/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('course/group-students/create/', GroupStudentCreateView.as_view(), name='group_create'),
    path('course/group-students/<int:pk>/', GroupStudentDetailView.as_view(), name='group_detail'),
    path('course/table/create/', TableCreateView.as_view(), name='table_create'),
    path('course/table/<int:pk>/', TableDetailView.as_view(), name='table_detail'),
    path('course/table-type/create/', TableTypeCreateView.as_view(), name='table_type_create'),
    path('course/table-type/<int:pk>/', TableTypeDetailView.as_view(), name='table_type_detail'),
    path('course/rooms/create/', RoomsCreateView.as_view(), name='rooms_create'),
    path('course/rooms/<int:pk>/', RoomsDetailView.as_view(), name='rooms_detail'),
]