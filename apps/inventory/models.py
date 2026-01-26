from django.db import models

class Equipment(models.Model):
    EQUIP_TYPE = [('SIMPLE', 'Outil Simple'), ('COMPOUND', 'Échafaudage/Kit')]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=EQUIP_TYPE, default='SIMPLE')
    daily_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_under_maintenance = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Component(models.Model):
    """Pièces individuelles : Cadre, Croisée, Roue, etc."""
    equipment = models.ForeignKey(Equipment, related_name='components', on_delete=models.CASCADE)
    name = models.CharField(max_length=100) 
    total_quantity = models.PositiveIntegerField()
    
    def available_quantity(self):
        # Logique de calcul soustrayant les pièces en location active
        pass
