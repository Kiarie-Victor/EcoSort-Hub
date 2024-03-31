from django.db import models
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

User = get_user_model()

# Message model representing individual chat messages


class Message(models.Model):
    body = models.TextField()  # Body of the message
    # User who sent the message
    sent_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # Timestamp of message creation
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)  # Ordering messages by creation timestamp

    def __str__(self):
        # String representation of the message (sender's username)
        return self.sent_by.username

    # Method to retrieve the last 20 messages from the database
    async def get_last_20_messages(self):
        # Asynchronously fetch the last 20 messages from the database
        messages = await sync_to_async(Message.objects.order_by('created_at').all()[:20])
        return messages
