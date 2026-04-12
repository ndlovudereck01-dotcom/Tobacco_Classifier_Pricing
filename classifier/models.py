from django.db import models
from django.utils import timezone
import os
import uuid
from django.contrib.auth.models import User

def tobacco_image_path(instance, filename):
    """Generate unique file path for uploaded tobacco images."""
    # Get the file extension
    ext = filename.split('.')[-1]
    # Generate a unique filename with timestamp
    filename = f"{uuid.uuid4().hex}_{int(timezone.now().timestamp())}.{ext}"
    # Return the upload path
    return os.path.join('tobacco_images', filename)

class TobaccoImage(models.Model):
    """Model to store uploaded tobacco images."""
    image = models.ImageField(upload_to=tobacco_image_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_tobacco = models.BooleanField(null=True)
    blur_score = models.FloatField(null=True, blank=True)
    
    # Farmer information fields
    group = models.CharField(max_length=50, blank=True)
    grower_number = models.CharField(max_length=50, blank=True)
    lot_number = models.CharField(max_length=50, blank=True)
    bale_number = models.CharField(max_length=50, blank=True)
    weight = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"Tobacco Image {self.id}"
    
    class Meta:
        ordering = ['-uploaded_at']

class ClassificationResult(models.Model):
    """Model to store tobacco classification results."""
    tobacco_image = models.OneToOneField(TobaccoImage, on_delete=models.CASCADE, related_name='result')
    grade = models.CharField(max_length=20)
    confidence = models.FloatField()
    price = models.FloatField()
    classified_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Classification for {self.tobacco_image} - Grade: {self.grade}"
    
    class Meta:
        ordering = ['-classified_at']

class Rating(models.Model):
    """Model to store user ratings and comments about the application."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.rating} stars - {self.created_at}"
    
    @classmethod
    def get_average_rating(cls):
        """Calculate and return the average rating."""
        ratings = cls.objects.all()
        if not ratings:
            return 0
        total = sum(rating.rating for rating in ratings)
        return round(total / len(ratings), 2)
