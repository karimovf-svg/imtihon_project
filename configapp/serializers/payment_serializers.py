from rest_framework import serializers

from ..models import *


class MonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Month
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    payment_type = serializers.SlugRelatedField(queryset=PaymentType.objects.all(), slug_field='title')
    month = serializers.SlugRelatedField(queryset=Month.objects.all(), slug_field='title')

    class Meta:
        model = Payment
        fields = ['id', 'student', 'group', 'month', 'payment_type','created_ed', 'updated_ed', 'price']


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = '__all__'