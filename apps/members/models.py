from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=100) 
    post_name = models.CharField(max_length=100, blank=True) 
    phone = models.CharField(max_length=20, unique=True) 
    address = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.post_name}"