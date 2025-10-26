from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils import timezone
from django.contrib.auth import authenticate
import hashlib
import time
import base64

class SignUpForm(UserCreationForm):
    """Form for user signup."""
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
        
class CustomLoginForm(AuthenticationForm):
    """Custom login form with styled widgets and security features."""
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Password'
        })
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        # Check if user is blocked
        cache_key = f'login_attempts_{username}'
        attempts = cache.get(cache_key, 0)
        block_until = cache.get(f'block_until_{username}')
        
        if block_until and time.time() < block_until:
            remaining_time = int(block_until - time.time())
            raise forms.ValidationError(
                f'Too many failed attempts. Please try again in {remaining_time} seconds.'
            )
        
        if username and password:
            # Verify the password using Django's authenticate function
            user = authenticate(request=self.request, username=username, password=password)
            if user is None:
                # Increment failed attempts
                attempts += 1
                cache.set(cache_key, attempts, 3600)  # Store attempts for 1 hour
                
                if attempts >= 5:
                    # Block for 30 seconds
                    cache.set(f'block_until_{username}', time.time() + 30, 30)
                    raise forms.ValidationError(
                        'Too many failed attempts. Please try again in 30 seconds.'
                    )
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                # Reset attempts on successful login
                cache.delete(cache_key)
                cache.delete(f'block_until_{username}')
                self.user_cache = user  # Set the user_cache as required by AuthenticationForm
        
        return self.cleaned_data

class UserUpdateForm(forms.ModelForm):
    """Form for updating user details."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']