from django.urls import path
from .views import stipendDeleteView, stipendUpdateView, stipendCreateView, expenseCreateView, expenseListView, expenseUpdateView, expenseDeleteView
from . import views


urlpatterns = [
    # path('', stipendListView.as_view(), name='budget-home'),
    path('', views.home, name='budget-home'),
    path('about/', views.about, name='budget-about'),
    path('stipend/new/', stipendCreateView.as_view(), name='stipend-create'),
    path('stipend/<int:pk>/update/', stipendUpdateView.as_view(), name='stipend-update'),
    path('stipend/<int:pk>/delete/', stipendDeleteView.as_view(), name='stipend-delete'),
    path('expense/new/', expenseCreateView.as_view(), name='expense-create'),
    path('expenses/', expenseListView.as_view(), name='expense-list'),
    path('expense/<int:pk>/update/', expenseUpdateView.as_view(), name='expense-update'),
    path('expense/<int:pk>/delete/', expenseDeleteView.as_view(), name='expense-delete'),
]