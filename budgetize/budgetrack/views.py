
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.db.models import Count

# from .schema import server_list_docs
from .models import IncomeStream, Expense
from .serializer import ExpenseSerializer

# endpoint setup
class ExpensesListViewSet(viewsets.ViewSet):
    queryset = Expense.objects.all()
    incomequery = IncomeStream.objects.all()

    @server_list_docs
    def list(self, request):
        """schema comes here
        """
        # Sample data representing servers
        IncomeStream = request.query_params.get('income_stream')
        amount = request.query_params.get('amount') # default to 10 if not provided
        title = request.query_params.get('name') 
        category = request.query_params.get('category')
        date = request.query_params.get("date")
        currency = request.query_params.get("currecncy")
        paid = request.query_params.get("paid") == "true"
        frequency = request.query_params.get("frequency")
        
        
        '''
        order of if statements is the order of appearents in search bar
        '''

        # # must be logged in
        # if by_user or by_serverID and not request.user.is_authenticated:
        #     raise AuthenticationFailed()
        
        if category:
            # convert to JSON so it can be sent over to the frontend
            # done using a serializer
            self.queryset = self.queryset.filter(category__name=category) #updating queryset to filter by category name
                    
        if amount:
            self.queryset = self.queryset[:int(amount)] # filter and return amount 

        if date:
            self.queryset = self.queryset[:int(date)] # filter by date

        if title:
            self.queryset = self.queryset.filter(title__name=title) # filter by title of expense

        if frequency:
            self.incomequery = self.incomequery.filter(frequency__name=frequency)
        
        if paid:
            self.queryset = self.queryset.filter(paid=paid) # updating queryset to filter by status of payment

    
        # passing the above filters to the serializer   
        serializer = ExpenseSerializer(self.queryset, many=True)
        return Response(serializer.data)

    