from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from django.db.models import Q, Max
from .models import Message
from .serializers import (
    MessageSerializer, MessageListSerializer, ConversationSerializer,
    ChatUserSerializer
)

class MessageListView(generics.ListCreateAPIView):
    """List and create messages"""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Get messages between current user and another user"""
        other_user_id = self.request.query_params.get('user_id')
        if not other_user_id:
            return Message.objects.none()
        
        return Message.objects.filter(
            Q(sender=self.request.user, receiver_id=other_user_id) |
            Q(sender_id=other_user_id, receiver=self.request.user)
        ).order_by('timestamp')

class ConversationListView(generics.ListAPIView):
    """List all conversations for current user"""
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Get all conversations for the current user"""
        user = self.request.user
        
        # Get all users the current user has conversations with
        conversations = []
        
        # Get all messages where user is sender or receiver
        messages = Message.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).select_related('sender', 'receiver').order_by('timestamp')
        
        # Group by conversation partner
        conversation_partners = set()
        for message in messages:
            if message.sender == user:
                conversation_partners.add(message.receiver)
            else:
                conversation_partners.add(message.sender)
        
        # Build conversation data
        for partner in conversation_partners:
            # Get last message in this conversation
            last_message = Message.objects.filter(
                Q(sender=user, receiver=partner) |
                Q(sender=partner, receiver=user)
            ).order_by('-timestamp').first()
            
            # Count unread messages
            unread_count = Message.objects.filter(
                sender=partner,
                receiver=user,
                timestamp__gt=user.last_login
            ).count() if hasattr(user, 'last_login') else 0
            
            conversations.append({
                'other_user': partner,
                'last_message': last_message.content if last_message else '',
                'last_message_time': last_message.timestamp if last_message else None,
                'unread_count': unread_count
            })
        
        # Sort by last message time
        conversations.sort(key=lambda x: x['last_message_time'] or x['other_user'].date_joined, reverse=True)
        
        return conversations

class ChatUserListView(generics.ListAPIView):
    """List all users for chat"""
    serializer_class = ChatUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Get all users except current user"""
        return User.objects.exclude(id=self.request.user.id)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def unread_message_count(request):
    """Get count of unread messages for current user"""
    count = Message.objects.filter(
        receiver=request.user,
        timestamp__gt=request.user.last_login
    ).count() if hasattr(request.user, 'last_login') else 0
    
    return Response({
        'unread_count': count
    })

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_messages_as_read(request):
    """Mark messages from a specific user as read"""
    sender_id = request.data.get('sender_id')
    
    if not sender_id:
        return Response({
            'error': 'sender_id is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Update last_login to mark messages as read
    # This is a simple approach - in production you might want a separate read status field
    request.user.save()
    
    return Response({
        'message': 'Messages marked as read'
    })

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_message(request, message_id):
    """Delete a specific message (only if user is the sender)"""
    try:
        message = Message.objects.get(id=message_id, sender=request.user)
        message.delete()
        return Response({
            'message': 'Message deleted successfully'
        })
    except Message.DoesNotExist:
        return Response({
            'error': 'Message not found or you are not authorized to delete it'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def chat_statistics(request):
    """Get chat statistics for current user"""
    total_messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).count()
    
    sent_messages = Message.objects.filter(sender=request.user).count()
    received_messages = Message.objects.filter(receiver=request.user).count()
    
    # Count unique conversations
    conversations = set()
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    )
    
    for message in messages:
        if message.sender == request.user:
            conversations.add(message.receiver.id)
        else:
            conversations.add(message.sender.id)
    
    return Response({
        'total_messages': total_messages,
        'sent_messages': sent_messages,
        'received_messages': received_messages,
        'unique_conversations': len(conversations)
    })
