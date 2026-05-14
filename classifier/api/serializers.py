from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from classifier.models import ClassificationResult, TobaccoImage


class ClassificationResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassificationResult
        fields = ['grade', 'confidence', 'price', 'classified_at']


class TobaccoImageSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()

    class Meta:
        model = TobaccoImage
        fields = [
            'id',
            'image',
            'uploaded_at',
            'is_tobacco',
            'blur_score',
            'group',
            'grower_number',
            'lot_number',
            'bale_number',
            'weight',
            'result',
        ]

    def get_result(self, obj):
        try:
            res = obj.result
        except ObjectDoesNotExist:
            return None
        return ClassificationResultSerializer(res).data
