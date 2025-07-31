from rest_framework import serializers
from .models import Message
from django.contrib.auth.models import User

class UserBasicSerializer(serializers.ModelSerializer):
    """Basic user serializer for chat"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class MessageSerializer(serializers.ModelSerializer):
    """Main message serializer"""
    sender = UserBasicSerializer(read_only=True)
    receiver = UserBasicSerializer(read_only=True)
    receiver_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'receiver_id', 'content', 'timestamp']
        read_only_fields = ['id', 'sender', 'timestamp']

    def create(self, validated_data):
        receiver_id = validated_data.pop('receiver_id')
        validated_data['sender'] = self.context['request'].user
        validated_data['receiver'] = User.objects.get(id=receiver_id)
        return super().create(validated_data)

class MessageListSerializer(serializers.ModelSerializer):
    """Simplified message serializer for listing"""
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)
    receiver_name = serializers.CharField(source='receiver.get_full_name', read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'sender_name', 'receiver_name', 'content', 'timestamp']

class ConversationSerializer(serializers.Serializer):
    """Serializer for conversation data"""
    other_user = UserBasicSerializer()
    last_message = serializers.CharField()
    last_message_time = serializers.DateTimeField()
    unread_count = serializers.IntegerField()

class ChatUserSerializer(serializers.ModelSerializer):
    """Serializer for users in chat list"""
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'unread_count']
    
    def get_unread_count(self, obj):
        request_user = self.context['request'].user
        return Message.objects.filter(
            sender=obj, 
            receiver=request_user, 
            timestamp__gt=request_user.last_login
        ).count() if hasattr(request_user, 'last_login') else 0 