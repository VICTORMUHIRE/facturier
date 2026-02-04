from django.db import transaction
from rest_framework import serializers
from ..models import Equipment, EquipmentUnit, Component

class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ['id', 'name', 'quantity_required']
        
class EquipmentUnitSerializer(serializers.ModelSerializer):
    equipment_name = serializers.ReadOnlyField(source='equipment.name')
    equipment_price = serializers.ReadOnlyField(source='equipment.daily_price')
    class Meta:
        model = EquipmentUnit
        fields = ['id', 'internal_code', 'status', 'equipment_name', 'equipment_price']

class EquipmentSerializer(serializers.ModelSerializer):
    components = ComponentSerializer(many=True, required=False)
    units = EquipmentUnitSerializer(many=True, required=False)
    available_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Equipment
        fields = ['id', 'name', 'ref_code', 'category', 'daily_price', 'components', 'units', 'available_count']

    def get_available_count(self, obj):
        return obj.units.filter(status='AVAILABLE').count()
    
    @transaction.atomic
    def create(self, validated_data):
        # On extrait les données imbriquées qui ont été validées (sans le champ equipment)
        components_data = validated_data.pop('components', [])
        units_data = validated_data.pop('units', [])
        
        # Création de l'équipement
        equipment = Equipment.objects.create(**validated_data)

        # Création des enfants en injectant l'instance equipment
        for comp in components_data:
            Component.objects.create(equipment=equipment, **comp)

        for unit in units_data:
            EquipmentUnit.objects.create(equipment=equipment, **unit)

        return equipment