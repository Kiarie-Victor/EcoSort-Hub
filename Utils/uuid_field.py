import uuid
from django.db import models


class UUIDGenerator(models.Model):
    # Define a primary key field using UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        # Set the model as abstract so it can be used as a base class for other models
        abstract = True

