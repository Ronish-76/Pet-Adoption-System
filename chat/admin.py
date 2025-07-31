from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content_preview', 'timestamp')
    list_filter = ('timestamp', 'sender', 'receiver')
    search_fields = ('sender__username', 'receiver__username', 'content')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('Message Information', {
            'fields': ('sender', 'receiver', 'content')
        }),
        ('Timestamps', {
            'fields': ('timestamp',),
            'classes': ('collapse',)
        }),
    )
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('sender', 'receiver')
    
    actions = ['delete_old_messages']
    
    def delete_old_messages(self, request, queryset):
        # This is just an example action - you might want to implement actual logic
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{count} messages were successfully deleted.')
    delete_old_messages.short_description = "Delete selected messages"
