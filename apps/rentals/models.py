from django.db import models
from django.conf import settings
from datetime import timedelta

class Rental(models.Model):
    STATUS = [
        ('PENDING', 'En attente'), 
        ('ACTIVE', 'En cours'), 
        ('FINISHED', 'Terminé'), 
        ('EXTENDED', 'Prolongé'),
        ('CANCELLED', 'Annulé')
    ]
    
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    member = models.ForeignKey('members.Member', on_delete=models.CASCADE)
    unit = models.ForeignKey('inventory.EquipmentUnit', on_delete=models.PROTECT, related_name='rentals')
    
    date_start = models.DateField() 
    date_end_expected = models.DateField() 
    actual_end_date = models.DateField(null=True, blank=True)
    
    # Finances
    daily_rate_at_time = models.DecimalField(max_digits=10, decimal_places=2, help_text="Prix/jour au moment de la signature")
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Hors charges
    transport_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    setup_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    
    status = models.CharField(max_length=10, choices=STATUS, default='ACTIVE')
    comment = models.TextField(blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_billable_days(self, start, end):
        """Calcule les jours entre start et end en excluant les dimanches"""
        days = 0
        current_date = start
        while current_date <= end:
            if current_date.weekday() != 6: # 6 = Dimanche en Python (0=Lundi)
                days += 1
            current_date += timedelta(days=1)
        return days

    @property
    def total_days(self):
        end = self.actual_end_date if self.actual_end_date else self.date_end_expected
        return self.calculate_billable_days(self.date_start, end)

    @property
    def total_rent_cost(self):
        return (self.total_days * self.daily_rate_at_time)

    @property
    def final_total(self):
        return (self.total_rent_cost - self.discount) + self.transport_fee + self.setup_fee

    @property
    def amount_paid(self):
        return sum(p.amount for p in self.payments.all())

    @property
    def amount_due(self):
        return self.final_total - self.amount_paid
    
class RentalExtension(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, related_name='extensions')
    old_end_date = models.DateField()
    new_end_date = models.DateField()
    extension_date = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        self.rental.date_end_expected = self.new_end_date
        self.rental.status = 'EXTENDED'
        self.rental.save()
        super().save(*args, **kwargs)


class Payment(models.Model):
    rental = models.ForeignKey(Rental, related_name='payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2) 
    date_paid = models.DateTimeField(auto_now_add=True)
    is_advance = models.BooleanField(default=True) 
    
    class Meta:
        ordering = ['-date_paid'] 
