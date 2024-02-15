from django.db import models

# Create your models here.

class DidYouKnow(models.Model):
    message = models.TextField()
