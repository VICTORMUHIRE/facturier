from rest_framework import serializers
from ..models import Equipment, EquipmentUnit, Component

class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ['id', 'name', 'quantity_required']

class EquipmentUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentUnit
        fields = ['id', 'internal_code', 'status']

class EquipmentSerializer(serializers.ModelSerializer):
    # On imbrique tout pour le front
    components = ComponentSerializer(many=True, read_only=True)
    units = EquipmentUnitSerializer(many=True, read_only=True)
    
    # Champ calculé : nombre d'unités disponibles
    available_count = serializers.SerializerMethodField()

    class Meta:
        model = Equipment
        fields = ['id', 'name', 'category', 'daily_price', 'components', 'units', 'available_count']

    def get_available_count(self, obj):
        return obj.units.filter(status='AVAILABLE').count()