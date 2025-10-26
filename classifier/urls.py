from django.urls import path
from . import views

app_name = 'classifier'

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_image, name='upload_image'),
    path('camera/', views.camera_upload, name='camera_upload'),
    path('result/<int:image_id>/', views.result, name='result'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search-farmer/', views.search_farmer, name='search_farmer'),
    path('api/statistics/', views.get_statistics, name='get_statistics'),
    path('api/grade-distribution/', views.get_grade_distribution, name='get_grade_distribution'),
    path('api/price-history/', views.get_price_history, name='get_price_history'),
    path('ratings/', views.ratings_list, name='ratings_list'),
    path('ratings/delete/<int:rating_id>/', views.delete_rating, name='delete_rating'),
]
