from django.contrib import admin
from .models import TobaccoImage, ClassificationResult

@admin.register(TobaccoImage)
class TobaccoImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'uploaded_at', 'is_tobacco')
    list_filter = ('is_tobacco', 'uploaded_at')
    search_fields = ('id',)

@admin.register(ClassificationResult)
class ClassificationResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'tobacco_image', 'grade', 'confidence', 'price', 'classified_at')
    list_filter = ('grade', 'classified_at')
    search_fields = ('grade', 'tobacco_image__id')
