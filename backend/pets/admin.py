from django.contrib import admin
from .models import Pet, Shelter, User, AdoptionRequest

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['name', 'pet_type', 'breed', 'age', 'status', 'shelter']
    list_filter = ['pet_type', 'status', 'gender', 'size']
    search_fields = ['name', 'breed']

@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at']
    search_fields = ['name', 'email']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'full_name', 'created_at']
    search_fields = ['username', 'email', 'full_name']

@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ['pet', 'user', 'status', 'request_date']
    list_filter = ['status', 'request_date']