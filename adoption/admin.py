from django.contrib import admin
from .models import AdoptionRequest

@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'pet', 'status', 'created', 'get_user_email', 'get_pet_type')
    list_filter = ('status', 'created', 'pet__pet_type')
    search_fields = ('user__username', 'user__email', 'pet__name', 'reason')
    readonly_fields = ('created',)
    list_editable = ('status',)
    date_hierarchy = 'created'
    
    fieldsets = (
        ('Request Information', {
            'fields': ('user', 'pet', 'status')
        }),
        ('Details', {
            'fields': ('reason', 'created')
        }),
    )
    
    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'User Email'
    
    def get_pet_type(self, obj):
        return obj.pet.pet_type
    get_pet_type.short_description = 'Pet Type'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'pet')
    
    actions = ['approve_requests', 'reject_requests']
    
    def approve_requests(self, request, queryset):
        updated = queryset.update(status='approved')
        # Update pet status to adopted
        for adoption in queryset:
            adoption.pet.status = 'adopted'
            adoption.pet.save()
        self.message_user(request, f'{updated} adoption requests were successfully approved.')
    approve_requests.short_description = "Approve selected adoption requests"
    
    def reject_requests(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} adoption requests were successfully rejected.')
    reject_requests.short_description = "Reject selected adoption requests"
