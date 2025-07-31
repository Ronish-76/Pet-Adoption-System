from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_phone', 'get_city')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'profile__is_shelter')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'profile__phone_number', 'profile__city')
    
    def get_phone(self, obj):
        return obj.profile.phone_number if hasattr(obj, 'profile') else '-'
    get_phone.short_description = 'Phone'
    
    def get_city(self, obj):
        return obj.profile.city if hasattr(obj, 'profile') else '-'
    get_city.short_description = 'City'

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'city', 'state', 'is_shelter', 'shelter_name')
    list_filter = ('is_shelter', 'state')
    search_fields = ('user__username', 'user__email', 'phone_number', 'city', 'shelter_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'phone_number', 'bio', 'profile_picture')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'zip_code')
        }),
        ('Shelter Information', {
            'fields': ('is_shelter', 'shelter_name', 'shelter_description'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
