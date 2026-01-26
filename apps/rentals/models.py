from django.db import models
from django.conf import settings

class Rental(models.Model):
    STATUS = [('ACTIVE', 'En cours'), ('FINISHED', 'Terminé'), ('EXTENDED', 'Prolongé')]
    
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    member = models.ForeignKey('members.Member', on_delete=models.CASCADE)
    equipment = models.ForeignKey('inventory.Equipment', on_delete=models.PROTECT)
    
    date_start = models.DateField() 
    date_end_expected = models.DateField() 
    
    # Finances
    total_amount_initial = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Hors charges
    transport_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    setup_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    
    status = models.CharField(max_length=10, choices=STATUS, default='ACTIVE')
    comment = models.TextField(blank=True) 

    @property
    def final_total(self):
        return (self.total_amount_initial - self.discount) + self.transport_fee + self.setup_fee

    @property
    def amount_due(self):
        # Somme restant due après le paiement [cite: 40]
        total_paid = sum(p.amount for p in self.payments.all())
        return self.final_total - total_paid

class Payment(models.Model):
    rental = models.ForeignKey(Rental, related_name='payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2) 
    date_paid = models.DateTimeField(auto_now_add=True)
    is_advance = models.BooleanField(default=True) 
    
    class Meta:
        ordering = ['-date_paid'] 
