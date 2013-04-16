from django.db import models

# Base class that all model classes inherit from
# Ensures that all models have a created and modified
# date fields for tracking
class TimeStampedModel(models.Model):
    """
    Abstract base class that provides self
    updating created and modified fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
