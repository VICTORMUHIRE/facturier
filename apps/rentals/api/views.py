from rest_framework import viewsets
from rest_framework.response import Response
from django.db import transaction
from ..models import Rental
from .serializers import RentalSerializer
from rest_framework.decorators import action
from datetime import datetime


class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all().order_by('-created_at')
    serializer_class = RentalSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        # 1. Sauvegarder la location
        rental = serializer.save(manager=self.request.user)
        
        # 2. Mettre à jour le statut de l'unité physique
        unit = rental.unit
        unit.status = 'RENTED'
        unit.save()

    @transaction.atomic
    def destroy(self, instance):
        """Si on supprime une location (erreur de saisie), on libère l'unité"""
        unit = instance.unit
        unit.status = 'AVAILABLE'
        unit.save()
        instance.delete()


    @action(detail=False, methods=['post'])
    def estimate_price(self, request):
        """Calcule le prix sans enregistrer en base de données"""
        try:
            start = datetime.strptime(request.data.get('date_start'), '%Y-%m-%d').date()
            end = datetime.strptime(request.data.get('date_end_expected'), '%Y-%m-%d').date()
            daily_rate = float(request.data.get('daily_rate', 0))
            discount = float(request.data.get('discount', 0))
            
            # Utilisation de la logique du modèle (hors instance)
            dummy_rental = Rental(date_start=start, date_end_expected=end)
            days = dummy_rental.calculate_billable_days(start, end)
            
            total = (days * daily_rate) - discount
            
            return Response({
                'billable_days': days,
                'estimated_total': max(0, total),
                'message': f"Calcul basé sur {days} jours ouvrables (hors dimanches)."
            })
        except Exception as e:
            return Response({'error': str(e)}, status=400)