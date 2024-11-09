from django.db import models  # Import the models module to define the database model
from django.contrib.auth.models import User  # Import the User model from Django's auth system

class WeightEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key relationship to the User model
    date = models.DateField(auto_now_add=True)  # Automatically set the date when the entry is created
    weight = models.DecimalField(max_digits=5, decimal_places=2)  # Decimal field to store the weight value with precision
