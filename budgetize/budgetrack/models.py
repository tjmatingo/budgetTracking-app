from django.db import models

# Create your models here.
class IncomeStream(models.Model):
    title = models.CharField(max_length=100)  # Name of the income source (e.g., "Freelance", "Salary")
    amount = models.DecimalField(max_digits=12, decimal_places=2)  # Income amount per period
    frequency = models.CharField(
        max_length=20,
        choices=[('daily','Daily'), ('weekly','Weekly'), ('monthly','Monthly'), ('yearly','Yearly')]
    )
    start_date = models.DateField()  # When the income stream started    
    currency = models.CharField(max_length=10, default='USD')

    def __str__(self):
        return f"{self.name} - {self.amount} {self.currency}"
    

class Expense(models.Model):
    income_stream = models.ForeignKey(
        'IncomeStream', 
        on_delete=models.CASCADE,  # if income stream is deleted, expenses get deleted too
        related_name='expenses'
    )
    title = models.CharField(max_length=100)  # Name of the expense (e.g., "Rent", "Groceries")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(
        max_length=50,
        choices=[('Luxury','Luxury'), ('subscriptions','Subscriptions'), ('groceries','Groceries'), ('transport','Transport'), ('other','Other')]
    )
    date = models.DateField()  # When the expense was made
    currency = models.CharField(max_length=10, default='USD')
    notes = models.TextField(blank=True, null=True)  # Any extra details
    paid = models.BooleanField(default=True)  # Has this expense been paid?


    def clean(self):
        # Calculate total expenses for this income stream (excluding this instance if updating)
        total_expenses = self.income_stream.expenses.exclude(pk=self.pk).aggregate(
            total=models.Sum('amount')
        )['total'] or 0

        if total_expenses + self.amount > self.income_stream.amount:
            raise ValidationError(
                f"Total expenses ({total_expenses + self.amount}) is more than the income ({self.income_stream.amount})."
            )
        
    def save(self, *args, **kwargs):
        self.clean()  # ensure validation runs on save
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} expense - {self.amount}"
    
    