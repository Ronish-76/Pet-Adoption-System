from django.db import models
from django.contrib.auth.models import User

class Pet(models.Model):
    PET_TYPES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('fish', 'Fish'),
        ('rabbit', 'Rabbit'),
        ('other', 'Other'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('unknown', 'Unknown'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('adopted', 'Adopted'),
        ('pending', 'Pending'),
    ]
    
    name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=20, choices=PET_TYPES)
    breed = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField(help_text="Age in years")
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.age < 0 or self.age > 30:
            raise ValidationError('Age must be between 0 and 30 years')
        if not self.name.strip():
            raise ValidationError('Pet name cannot be empty')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    image = models.ImageField(upload_to='pets/', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_pets', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_pet_type_display()}"
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'pet_type']),
            models.Index(fields=['created_at']),
        ]
