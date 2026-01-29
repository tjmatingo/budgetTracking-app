from django.db import models
from django.utils import timezone

# Create your models here.
class Stipend(models.Model):
    name = models.CharField(max_length=100)
    month = models.CharField(max_length=20)
    stipend_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class Expense(models.Model):
    stipend = models.ForeignKey(Stipend, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_incurred = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.description} - {self.amount}"