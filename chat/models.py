from django.db import models
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

User = get_user_model()

# Create your models here.
class Message(models.Model):
    body = models.TextField()
    sent_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.sent_by

    async def get_last_20_messages(self):
        messages = await sync_to_async(Message.objects.order_by('create_at').all()[:21])
        return messages
    