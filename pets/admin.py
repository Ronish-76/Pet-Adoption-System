from django.contrib import admin
from .models import Pet

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'pet_type', 'breed', 'age', 'gender', 'status', 'owner', 'created_at')
    list_filter = ('pet_type', 'gender', 'status', 'created_at')
    search_fields = ('name', 'breed', 'description', 'owner__username')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'pet_type', 'breed', 'age', 'gender')
        }),
        ('Details', {
            'fields': ('description', 'image')
        }),
        ('Status', {
            'fields': ('status', 'owner')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('owner')
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new pet
            obj.owner = request.user
        super().save_model(request, obj, form, change)
