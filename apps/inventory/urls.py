from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views import EquipmentUnitViewSet, EquipmentViewSet, ComponentViewSet

router = DefaultRouter()
router.register(r'equipment', EquipmentViewSet, basename='equipment')
router.register(r'components', ComponentViewSet, basename='component')
router.register(r'units', EquipmentUnitViewSet, basename='unit') 


urlpatterns = [
    path('api/', include(router.urls)),
]