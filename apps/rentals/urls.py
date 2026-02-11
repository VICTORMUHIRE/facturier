from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views import RentalViewSet

router = DefaultRouter()
router.register(r'rentals', RentalViewSet)

urlpatterns = [
    path('api/', include(router.urls)),

]