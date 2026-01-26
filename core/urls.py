from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    # API endpoints
    path('api/auth/login/', auth_views.LoginView.as_view(), name='api-login'),
    path('api/auth/logout/', auth_views.LogoutView.as_view(), name='api-logout'),
    
    # Frontend routes
    path('login/', include('apps.frontend.urls')), 
]

