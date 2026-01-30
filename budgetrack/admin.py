from django.contrib import admin
from .models import Stipend, Expense
# Register your models here.

admin.site.register(Stipend)
admin.site.register(Expense)