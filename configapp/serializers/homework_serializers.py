from rest_framework import serializers
from ..models import *
from ..serializers import *

class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = '__all__'
        extra_kwargs = {'teacher': {'read_only': True}}

class HomeworkSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkSubmission
        fields = '__all__'
        extra_kwargs = {'student': {'read_only': True},
                        'is_checked': {'read_only': True}}

class HomeworkReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkReview
        fields = '__all__'
        extra_kwargs = {
            'teacher': {'read_only': True}
        }