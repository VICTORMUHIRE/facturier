from django.db import models

class Member(models.Model):
    TYPE_CHOICES = [
        ('PARTICULIER', 'Particulier'),
        ('ENTREPRISE', 'Entreprise/Organisation'),
    ]

    full_name = models.CharField(max_length=255, verbose_name="Nom Complet / Raison Sociale")
    client_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='PARTICULIER')
    phone = models.CharField(max_length=20, unique=True, verbose_name="Téléphone (+243...)")
    address = models.TextField(blank=True, null=True, verbose_name="Adresse Physique")
    id_card_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="N° Pièce d'Identité")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.full_name} "

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Membre"