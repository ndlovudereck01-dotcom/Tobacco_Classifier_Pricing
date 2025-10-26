from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomLoginForm

app_name = 'accounts'

urlpatterns = [
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        authentication_form=CustomLoginForm
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='accounts:login',
        template_name='accounts/login.html',
        http_method_names=['get', 'post']
    ), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    
    # Profile management
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password_view, name='change_password'),
    
    # User management (admin only)
    path('users/', views.users_list_view, name='users_list'),
]