from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()

# Create your models here.

class Message(models.Model):
    sender    = models.ForeignKey(User, related_name="sent", on_delete=models.CASCADE)
    receiver  = models.ForeignKey(User, related_name="received", on_delete=models.CASCADE)
    content   = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ("timestamp",)
