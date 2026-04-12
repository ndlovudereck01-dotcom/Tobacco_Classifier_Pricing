from django import forms
from .models import TobaccoImage, Rating
from django.core.validators import MinValueValidator, MaxValueValidator

class TobaccoImageForm(forms.ModelForm):
    class Meta:
        model = TobaccoImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

class ImageUploadForm(forms.Form):
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
            'id': 'imageUpload'
        })
    )
    group = forms.CharField(
        required=True,
        max_length=50,
        label='Group',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter group',
            'autocomplete': 'off',
        }),
    )
    grower_number = forms.CharField(
        required=True,
        max_length=50,
        label='Grower number',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter grower number',
            'autocomplete': 'off',
        }),
    )
    lot_number = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter lot number'
        })
    )
    weight = forms.FloatField(
        required=True,
        validators=[
            MinValueValidator(1, message="Weight must be at least 1 kg"),
            MaxValueValidator(120, message="Weight cannot exceed 120 kg")
        ],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter weight (1-120 kg)',
            'step': '0.01'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        # Add any additional validation logic here if needed
        return cleaned_data

class CameraUploadForm(forms.Form):
    image_data = forms.CharField(
        widget=forms.HiddenInput(attrs={'id': 'imageData'})
    )
    group = forms.CharField(
        required=True,
        max_length=50,
        label='Group',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter group',
            'autocomplete': 'off',
        }),
    )
    grower_number = forms.CharField(
        required=True,
        max_length=50,
        label='Grower number',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter grower number',
            'autocomplete': 'off',
        }),
    )
    lot_number = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter lot number',
            'autocomplete': 'off',
        }),
    )
    weight = forms.FloatField(
        required=True,
        label='Mass (kg)',
        validators=[
            MinValueValidator(1, message='Mass must be at least 1 kg'),
            MaxValueValidator(120, message='Mass cannot exceed 120 kg'),
        ],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter mass (1–120 kg)',
            'step': '0.01',
            'autocomplete': 'off',
        }),
    )

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }
