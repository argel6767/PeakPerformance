from django.db import models

# Create your models here.
'''
Models for movements and muscles worked in said movements
'''

class Muscle(models.Model):
    MUSCLE_CATEGORIES = [('arms', 'Arms'), ('back', 'Back'), ('chest', 'Chest'),
                         ('core', 'Core'), ('legs', 'Legs'), ('shoulders', 'Shoulders'),]
    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=10, choices=MUSCLE_CATEGORIES, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']  # Alphabetical ordering

class Movement(models.Model):
    MOVEMENT_TYPES = [('strength', 'Strength'), ('cardio', 'Cardiovascular')]
    name = models.CharField(max_length=100, unique=True)
    muscles_worked = models.ManyToManyField(Muscle, related_name="movements")
    type = models.CharField(max_length=15, choices=MOVEMENT_TYPES, default='strength')
    movement_image_url = models.TextField(blank=True) # could use this in future to link to a S3 or Azure Storage that holds image of movement for frontend
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']