from datetime import timedelta

from django.db.models import Avg, Count
from django.db.models.functions import TruncDay
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from classifier.models import ClassificationResult, TobaccoImage

from .serializers import TobaccoImageSerializer


class StatisticsAPIView(APIView):
    """Daily processed image counts for the last 7 days (dashboard chart)."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        last_week = timezone.now() - timedelta(days=7)
        daily_counts = (
            TobaccoImage.objects.filter(uploaded_at__gte=last_week)
            .annotate(day=TruncDay('uploaded_at'))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )
        labels = []
        data = []
        for item in daily_counts:
            labels.append(item['day'].strftime('%Y-%m-%d'))
            data.append(item['count'])
        return Response({'labels': labels, 'data': data})


class GradeDistributionAPIView(APIView):
    """Grade counts for the grade distribution chart."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        grade_counts = (
            ClassificationResult.objects.values('grade')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        labels = [item['grade'] for item in grade_counts]
        data = [item['count'] for item in grade_counts]
        return Response({'labels': labels, 'data': data})


class PriceHistoryAPIView(APIView):
    """Average classified price by day for the last 30 days."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        last_month = timezone.now() - timedelta(days=30)
        price_history = (
            ClassificationResult.objects.filter(classified_at__gte=last_month)
            .annotate(day=TruncDay('classified_at'))
            .values('day')
            .annotate(avg_price=Avg('price'))
            .order_by('day')
        )
        labels = [item['day'].strftime('%Y-%m-%d') for item in price_history]
        data = [float(item['avg_price']) for item in price_history]
        return Response({'labels': labels, 'data': data})


class TobaccoImageViewSet(viewsets.ReadOnlyModelViewSet):
    """List and retrieve tobacco images with nested classification when present."""

    permission_classes = [IsAuthenticated]
    serializer_class = TobaccoImageSerializer
    queryset = TobaccoImage.objects.select_related('result').order_by('-uploaded_at')
