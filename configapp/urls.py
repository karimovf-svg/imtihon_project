from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    # Auth
    path('auth/post_send_otp/', PhoneSendOTP.as_view()),
    path('auth/post_v_otp/', VerifySMS.as_view()),
    path('auth/login/', LoginApi.as_view(), name='token_obtain_pair'),
