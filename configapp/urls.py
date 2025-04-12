from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('post_send_otp/', PhoneSendOTP.as_view()),
    path('post_v_otp/', VerifySMS.as_view()),
    path('register/', RegisterUserApi.as_view()),
    path('token/', LoginApi.as_view(), name='token_obtain_pair'),
    path('teacher/create/', TeacherCreateApi.as_view(), name='teacher-create'),
    path('student/create/', StudentCreateApi.as_view(), name='student-create'),
]