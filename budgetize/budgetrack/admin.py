from django.contrib import admin
from .models import Expense, IncomeStream

# Register your models here.
admin.site.register(Expense)
admin.site.register(IncomeStream)