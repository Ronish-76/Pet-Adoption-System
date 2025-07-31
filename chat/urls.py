from django.urls import path
from . import views

urlpatterns = [
    # Message endpoints
    path('messages/', views.MessageListView.as_view(), name='message-list'),
    path('messages/<int:message_id>/delete/', views.delete_message, name='delete-message'),
    
    # Conversation endpoints
    path('conversations/', views.ConversationListView.as_view(), name='conversation-list'),
    path('users/', views.ChatUserListView.as_view(), name='chat-users'),
    
    # Utility endpoints
    path('unread-count/', views.unread_message_count, name='unread-count'),
    path('mark-read/', views.mark_messages_as_read, name='mark-read'),
    path('statistics/', views.chat_statistics, name='chat-statistics'),
] 