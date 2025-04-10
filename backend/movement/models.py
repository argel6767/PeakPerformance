from django.db import models

'''
Models for movements and muscles worked in said movements
'''

class Muscle(models.Model):
    muscle_name = models.CharField(max_length=15, unique=True)

class Movement(models.Model):
    movement_name = models.CharField(max_length=100, unique=True)
    muscles_worked = models.ManyToManyField(Muscle, related_name="muscles_worked")