from django.urls import path
from django.contrib.auth import views as auth_views
from . import views, api_views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),

    # Authentification
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html',redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('api/login/', api_views.login_api, name='api_login'),

    # membres
    path('members/', views.liste_membres, name='members_list'),
    
]