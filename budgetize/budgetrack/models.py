from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError

# Create your models here.
class IncomeStream(models.Model):
    title = models.CharField(max_length=100)  # Name of the income source (e.g., "Freelance", "Salary")
    amount = models.DecimalField(max_digits=12, decimal_places=2)  # Income amount per period
    frequency = models.CharField(
        max_length=20,
        choices=[('daily','Daily'), ('weekly','Weekly'), ('monthly','Monthly'), ('yearly','Yearly')]
    )
    remaining_balance = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    editable=False
    )
    start_date = models.DateField()  # When the income stream started    
    currency = models.CharField(max_length=10, default='USD')


    def update_remaining_balance(self):
        total_expenses = self.expenses.aggregate(
            total=Sum('amount')
        )['total'] or 0

        self.remaining_balance = self.amount - total_expenses
        self.save(update_fields=['remaining_balance'])

    def save(self, *args, **kwargs):
        # On first save, remaining balance = full income
        if self.pk is None:
            self.remaining_balance = self.amount
        super().save(*args, **kwargs)



    def __str__(self):
        return f"{self.title} - {self.amount} {self.currency}"
    

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
        # Remaining balance excluding this expense (important for updates)
        available_balance = self.income_stream.remaining_balance

        if self.pk:
            previous_amount = Expense.objects.get(pk=self.pk).amount
            available_balance += previous_amount

        if self.amount > available_balance:
            raise ValidationError(
                f"Expense exceeds remaining balance ({available_balance})."
            )
        
    def delete(self, *args, **kwargs):
        income_stream = self.income_stream
        super().delete(*args, **kwargs)
        income_stream.update_remaining_balance()

    def save(self, *args, **kwargs):
        self.clean()  # ensure validation runs on save
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} expense - {self.amount}, remaining: ${self.income_stream.update_remaining_balance}"
    
    