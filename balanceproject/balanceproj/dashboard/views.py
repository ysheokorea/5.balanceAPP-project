from django.http.response import JsonResponse
from django.shortcuts import render
from incomes_app.models import Incomes
from expenses_app.models import Expenses

from django.contrib.auth.decorators import login_required

# Data time zone
import datetime

# Create your views here.
@login_required(login_url='authentication/login')
def index(request):
    dateValue=datetime.date.today()
    dateYear=dateValue.year
    dateMonth=dateValue.month

    # step1 : Instance crate
    incomes=Incomes.objects.filter(person=request.user, date__istartswith=str(dateYear)+'-'+str(dateMonth))
    expenses=Expenses.objects.filter(person=request.user, date__istartswith=str(dateYear)+'-'+str(dateMonth))

    totalValue_inc = 0
    totalValue_ex = 0

    # step2 : Extract source data from each Instance
    def get_source(incomes):
        return incomes.source

    def get_category(expenses):
        return expenses.category

    # step3 : repeat remove, set >> list
    source_list = list(set(map(get_source, incomes)))
    category_list = list(set(map(get_category, expenses)))

    # Each source sum all of the amount of Instance
    def get_incomes_source_amount(source):
        amount = 0
        filtered_by_source = incomes.filter(source=source)
        for item in filtered_by_source:
            amount += item.amount
        return amount
    def get_expenses_category_amount(category):
        amount_ex = 0
        filtered_by_category = expenses.filter(category=category)
        for item in filtered_by_category:
            amount_ex += item.amount
        return amount_ex

    # Finally calculate the sum of each source data in Instance
    
    for y in source_list:
        totalValue_inc += get_incomes_source_amount(y)
    for x in category_list:
        totalValue_ex += get_expenses_category_amount(x)        

    context={
        'total' : totalValue_inc,
        'total_ex' : totalValue_ex,
        'time' : datetime.date.today(),
    }
    return render(request, 'index.html', context)
    

    


def progress_bar(request):
    # step1 : Instance crate
    incomes=Incomes.objects.filter(person=request.user, date__istartswith='2021-10')
    finalrep={}

    # step2 : Extract source data from each Instance
    def get_source(incomes):
        return incomes.source

    # step3 : repeat remove, set >> list
    source_list = list(set(map(get_source, incomes)))

    # Each source sum all of the amount of Instance
    def get_incomes_source_amount(source):
        amount = 0
        filtered_by_source = incomes.filter(source=source)
        for item in filtered_by_source:
            amount += item.amount
        return amount

    # Finally calculate the sum of each source data in Instance
    for x in incomes:
        for y in source_list:
            finalrep[y]=get_incomes_source_amount(y)


    # data = incomes.values()
    return JsonResponse({'income_source_data' : finalrep}, safe=False)

def dashboard_incomes_summary(request):
    todays_date = datetime.date.today()
    # incomes = Incomes.objects.filter(person=request.user, date__gte=six_month_ago, date__lte=todays_date)
    incomes = Incomes.objects.filter(person=request.user, date__istartswith=(str(todays_date.year)+'-'+str(todays_date.month)))
    finalrep = {}

    def get_source(incomes):
        return incomes.source

    source_list = list(set(map(get_source, incomes)))

    def get_income_source_amount(source):
        amount = 0
        filtered_by_source = incomes.filter(source=source)
        for item in filtered_by_source:
            amount += item.amount
        return amount
    
    for x in incomes:
        for y in source_list:
            finalrep[y] = get_income_source_amount(y)

    return JsonResponse({'income_source_data' : finalrep}, safe=False)


def dashboard_expenses_summary(request):
    dateValue=datetime.date.today()
    dateYear=dateValue.year
    dateMonth=dateValue.month

    # step1 : Instance crate
    expenses=Expenses.objects.filter(person=request.user, date__istartswith=str(dateYear)+'-'+str(dateMonth))
    finalrep = {}

    def get_category(expenses):
        return expenses.category

    category_list = list(set(map(get_category, expenses)))

    def get_expenses_category_amount(category):
        amount_ex = 0
        filtered_by_category = expenses.filter(category=category)
        for item in filtered_by_category:
            amount_ex += item.amount
        return amount_ex
    
    for y in expenses:
        for x in category_list:
         finalrep[x] = get_expenses_category_amount(x) 

    return JsonResponse({'expense_category_data' : finalrep}, safe=False)




    


