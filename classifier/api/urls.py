from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'images', views.TobaccoImageViewSet, basename='tobaccoimage')

urlpatterns = [
    path('statistics/', views.StatisticsAPIView.as_view(), name='api_statistics'),
    path('grade-distribution/', views.GradeDistributionAPIView.as_view(), name='api_grade_distribution'),
    path('price-history/', views.PriceHistoryAPIView.as_view(), name='api_price_history'),
    path('', include(router.urls)),
]
