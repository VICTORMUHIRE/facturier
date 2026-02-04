from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views import MemberViewSet

router = DefaultRouter()
router.register(r'members', MemberViewSet, basename='member')

urlpatterns = [
    path('api/', include(router.urls)),
]