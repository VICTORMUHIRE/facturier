from rest_framework import serializers
from ..models import Rental

class RentalSerializer(serializers.ModelSerializer):
    billable_days = serializers.ReadOnlyField(source='total_days')
    total_cost = serializers.ReadOnlyField(source='final_total')
    amount_due = serializers.ReadOnlyField()

    class Meta:
        model = Rental
        fields = [
            'pk', 'manager', 'member', 'unit', 'date_start', 
            'date_end_expected', 'daily_rate_at_time', 'discount', 
            'transport_fee', 'setup_fee', 'status', 'comment',
            'billable_days', 'total_cost', 'amount_due'
        ]

    def validate(self, data):
        """Vérification de la disponibilité de l'unité"""
        unit = data.get('unit')
        if unit.status != 'AVAILABLE':
            raise serializers.ValidationError(
                {"unit": f"L'unité {unit.internal_code} n'est pas disponible (Statut actuel: {unit.get_status_display()})."}
            )
        
        if data['date_end_expected'] < data['date_start']:
            raise serializers.ValidationError("La date de fin ne peut pas être antérieure à la date de début.")
            
        return data