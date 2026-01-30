from django.db import models
from django.utils import timezone

# Create your models here.
class Stipend(models.Model):
    name = models.CharField(max_length=100)
    month = models.DateField()  # e.g. 2026-01-01
    stipend_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    
class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Subscriptions', 'Subscriptions'),
        ('Entertainment', 'Entertainment'),
        ('Other', 'Other'),
    ]


    stipend = models.ForeignKey(Stipend, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='NONE')
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_incurred = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.description} - {self.amount}"