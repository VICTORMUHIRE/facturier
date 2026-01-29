from rest_framework import viewsets
from ..models import Equipment, EquipmentUnit, Component
from .serializers import EquipmentSerializer, EquipmentUnitSerializer, ComponentSerializer

class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

class EquipmentUnitViewSet(viewsets.ModelViewSet):
    queryset = EquipmentUnit.objects.all()
    serializer_class = EquipmentUnitSerializer

class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer