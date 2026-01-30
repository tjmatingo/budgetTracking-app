import json
from django.shortcuts import render
from .models import Stipend, Expense
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.generic import CreateView, UpdateView, DeleteView,  ListView
from django.db.models import Sum
from django.db.models.functions import TruncMonth


'''
CReate API views for offline mode
# i have just created the static files but need the understanding down on the directorties and files to create the API views

@api_view(['GET'])
def get_tasks(request):
    return Response([...])
'''
# Description pages
def home(request):

    '''
    add total spent for each category for the chart
    get remaining stipend after expenses
    Get data for home page including expenses by category and stipend information

    '''
    expenses = (
        Expense.objects
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('category')
    )
    
    stipend = Stipend.objects.all()

    categories = [e['category'] for e in expenses]
    totals = [float(e['total']) for e in expenses]

    monthly_expenses = (
        Expense.objects
        .annotate(month=TruncMonth('date_incurred'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
        )

    
    context = {
        'title': 'Budget Dashboard',
        'categories': json.dumps(categories),
        'totals': json.dumps(totals),
        'expenses':expenses, 
        'exps': Expense.objects.all(),
        'stipend':stipend,
        'monthly_expenses': monthly_expenses,
        }

    
    return render(request, 'budgetrack/home.html', context=context)

def about(request):
    context = {'title': 'About Budgetize'}
    return render(request, 'budgetrack/about.html', context=context)


# Salarie CRUD pages
class stipendCreateView(CreateView):
    model = Stipend
    fields = ['name', 'month', 'stipend_amount']
    

# class stipendListView(ListView):
#     model = Stipend
#       # <app>/<model>_<viewtype>.html
#     context_object_name = 'stipends'


    

class stipendUpdateView(UpdateView):
    model = Stipend
    fields = ['name', 'month', 'stipend_amount']

class stipendDeleteView(DeleteView):
    model = Stipend
    success_url = '/'

# Expense CRUD pages derived from Stipend
class expenseCreateView(CreateView):
    '''
        ensure user can add more than stipend amount remaining
    '''
    model = Expense
    fields = ['description', 'amount', 'date_incurred', 'category', 'stipend']

class expenseListView(ListView):
    model = Expense
    template_name = 'budgetrack/home.html'
    context_object_name = 'expenses'
    ordering = ['-date_incurred']
    
class expenseUpdateView(UpdateView):
    model = Expense
    fields = ['description', 'amount', 'date_incurred', 'category', 'stipend']


class expenseDeleteView(DeleteView):
    model = Expense
    success_url = '/'