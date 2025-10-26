from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import SignUpForm, UserUpdateForm
from .models import UserActivity
from django.utils import timezone

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def log_activity(user, action, description='', request=None):
    """Helper function to log user activities."""
    ip_address = get_client_ip(request) if request else None
    UserActivity.objects.create(
        user=user,
        action=action,
        description=description,
        ip_address=ip_address
    )

def signup_view(request):
    """View for user registration."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            log_activity(user, 'login', 'User registered and logged in', request)
            messages.success(request, "Account created successfully.")
            return redirect('classifier:home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def profile_view(request):
    """View for user profile."""
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            log_activity(request.user, 'profile_update', 'Profile information updated', request)
            messages.success(request, "Your profile has been updated!")
            return redirect('accounts:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    # Get recent activities for the user
    recent_activities = request.user.activities.all()[:5]
    
    context = {
        'form': form,
        'password_change_url': 'accounts:change_password',
        'recent_activities': recent_activities,
    } 
    return render(request, 'accounts/profile.html', context)

@login_required
def users_list_view(request):
    """View for listing all users and their activities (admin only)."""
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('classifier:home')
    
    users = User.objects.all().order_by('-date_joined')
    
    # Get activities for each user
    user_activities = {}
    for user in users:
        user_activities[user.id] = user.activities.all()[:10]  # Last 10 activities per user
    
    context = {
        'users': users,
        'user_activities': user_activities,
    }
    return render(request, 'accounts/users_list.html', context)

@login_required
def change_password_view(request):
    """View for changing user password."""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Update the session to prevent the user from being logged out
            update_session_auth_hash(request, user)
            log_activity(request.user, 'password_change', 'Password changed', request)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    
    context = {
        'form': form,
    }
    
    return render(request, 'accounts/password_change.html', context)
