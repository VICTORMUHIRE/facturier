from django.db import models

class Equipment(models.Model):
    EQUIP_TYPE = [('SIMPLE', 'Outil Simple'), ('COMPOUND', 'Échafaudage / Kit')]
    
    name = models.CharField(max_length=150, verbose_name="Nom de l'équipement")
    category = models.CharField(max_length=10, choices=EQUIP_TYPE, default='SIMPLE')
    daily_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix journalier ($)")
    image = models.ImageField(upload_to='equipment/', blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
    
class EquipmentUnit(models.Model):
    STATUS_CHOICES = [
        ('AVAILABLE', 'Disponible'),
        ('RENTED', 'En Location'),
        ('MAINTENANCE', 'En Réparation'),
        ('LOST', 'Perdu/Hors service'),
    ]

    equipment = models.ForeignKey(Equipment, related_name='units', on_delete=models.CASCADE)
    internal_code = models.CharField(max_length=50, unique=True, verbose_name="Code Interne (ex: BET-001)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    
    def __str__(self):
        return f"{self.internal_code} - {self.equipment.name}"

class Component(models.Model):
    """Les pièces qui constituent le stock physique"""
    equipment = models.ForeignKey(Equipment, related_name='components', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="Nom de la pièce") 
    quantity_required = models.PositiveIntegerField(default=0, verbose_name="Quantité Totale en Stock")
    min_threshold = models.PositiveIntegerField(default=1, verbose_name="Seuil d'alerte")

    def __str__(self):
        return f"{self.name} - {self.equipment.name}"