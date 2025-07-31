from django.contrib.auth import get_user_model
from django.db import models
from pets.models import Pet

User = get_user_model()

class AdoptionRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected")
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "pet")
        ordering = ['-created']
        indexes = [
            models.Index(fields=['status', 'created']),
            models.Index(fields=['user', 'status']),
        ]
        
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.pet.status != 'available':
            raise ValidationError('Cannot create adoption request for unavailable pet')
        if self.user == self.pet.owner:
            raise ValidationError('Pet owner cannot adopt their own pet')
        
    def __str__(self):
        return f"{self.user} -> {self.pet} ({self.status})"
