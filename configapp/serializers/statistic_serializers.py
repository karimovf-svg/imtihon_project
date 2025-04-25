from rest_framework.fields import DateField
from rest_framework.serializers import Serializer


class DateFilterSerializer(Serializer):
    start_date = DateField(required=True)
    end_date = DateField(required=True)