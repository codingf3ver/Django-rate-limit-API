from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    message = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')

    
    def __str__(self):
        return self.message
