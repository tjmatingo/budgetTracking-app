from django.shortcuts import render
from .models import Stipend, Expense
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.generic import CreateView, UpdateView, DeleteView,  ListView, DetailView


'''
CReate API views for offline mode
# i have just created the static files but need the understanding down on the directorties and files to create the API views

@api_view(['GET'])
def get_tasks(request):
    return Response([...])
'''
# Description pages
def home(request):
    expenses = Expense.objects.all()
    stipend = Stipend.objects.all()

    context = {'expenses':expenses, 'stipend':stipend}
    return render(request, 'budgetrack/home.html', context=context)

def about(request):
    context = {}
    return render(request, 'budgetrack/about.html', context=context)


# Salarie CRUD pages
class stipendCreateView(CreateView):
    model = Stipend
    fields = ['name', 'month', 'stipend_amount']


class stipendListView(ListView):
    model = Stipend
    template_name = 'budgetrack/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'stipends'


    

class stipendUpdateView(UpdateView):
    model = Stipend
    fields = ['name', 'month', 'stipend_amount']

class stipendDeleteView(DeleteView):
    model = Stipend
    success_url = '/'

# Expense CRUD pages derived from Stipend
class expenseCreateView(CreateView):
    model = Expense
    fields = ['description', 'amount', 'date_incurred']

class expenseListView(ListView):
    model = Expense
    template_name = 'budgetrack/home.html'
    context_object_name = 'expenses'
    ordering = ['-date_incurred']
class expenseUpdateView(UpdateView):
    model = Expense
    fields = ['description', 'amount', 'date_incurred']


class expenseDeleteView(DeleteView):
    model = Expense
    success_url = '/'