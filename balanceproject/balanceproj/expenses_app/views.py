# General
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render,redirect

# Messages
from django.contrib import messages

# Login
from django.contrib.auth.decorators import login_required

# Database
from expenses_app.models import Category, Expenses

# JSON
import json

# Datetime
import datetime

# File export
import csv
import xlwt
from django.template.loader import get_template
from xhtml2pdf import pisa

# Create your views here.
@login_required(login_url='authentication/login')
def index(request):
    categories=Category.objects.all()
    expenses=Expenses.objects.filter(person=request.user)
    context = {
        'categories' : categories,
        'expenses' : expenses,
    }

    return render(request, 'expenses/index.html', context)

def add_expenses(request):
    categories = Category.objects.all()
    context = {
        'categories' : categories,
        'values' : request.POST,
    }

    if request.method == "GET":
        return render(request, 'expenses/add-expenses.html', context)

    if request.method == "POST":
        date=request.POST['date']
        category=request.POST['category']
        amount=request.POST['amount']
        description=request.POST['description']
        
        if not date:
            messages.error(request, 'Data is required')
            return redirect('/add-expenses')
        if not amount:
            messages.error(request, 'Amount is required')
            return redirect('/add-expenses')
        if not description:
            messages.error(request, 'Description is required')
            return redirect('/add-expenses')    
    Expenses.objects.create(person=request.user, date=date, category=category, amount=amount, description=description)
    messages.success(request, 'Expenses saved successfully')

    return redirect('/expenses')

def edit_expenses(request, id):
    categories = Category.objects.all()
    expenses = Expenses.objects.get(pk=id)
    context = {
        'categories' : categories,
        'expenses' : expenses,
        'values' : request.POST,
    }

    if request.method == "GET":
        return render(request, 'expenses/edit-expenses.html', context)
    if request.method == "POST":
        date = request.POST['date']
        category = request.POST['category']
        amount = request.POST['amount']
        description = request.POST['description']

        if not amount:
            messages.error(request, 'Amount is required')
            return redirect('/add-expenses')
        if not description:
            messages.error(request, 'Description is required')
            return redirect('/add-expenses')    
        
        expenses.person = request.user
        if not date:
            expenses.date = expenses.date
        expenses.category = category
        expenses.amount = amount
        expenses.description = description
        expenses.save()

        messages.success(request, 'Expenses edit successfully')
        return redirect('/expenses')

def del_expenses(request, id):
    # step1. filter instances
    # step2. delete instances
    # step3. success message
    # step4. redirect expenses index page
    expenses = Expenses.objects.get(pk=id)
    expenses.delete()
    messages.success(request, 'Expenses successfully deleted')
    return redirect('/expenses')

def search_expenses(request):
    # step1. Receive json data(response)
    # step2. Filter Database based on the data from json
    # step3. Response with JsonResponse
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText')

        expenses = Expenses.objects.filter(
            amount__istartswith=search_str,  person=request.user) | Expenses.objects.filter(
            date__istartswith=search_str, person=request.user) | Expenses.objects.filter(
            description__icontains=search_str, person=request.user) | Expenses.objects.filter(
            category__icontains=search_str, person=request.user)

        data = expenses.values()
        return JsonResponse(list(data), safe=False)
        


def stats_expenses(request):
    return render(request, 'expenses/stats-expenses.html')

def summary_expenses(request):
    if request.method == 'POST':
        year_val=json.loads(request.body).get('yearVal')
        month_val=json.loads(request.body).get('monthVal')
        expenses=Expenses.objects.filter(person=request.user, date__istartswith=(year_val+'-'+month_val))
        finalrep={}

        def get_category(expenses):
            return expenses.category

        source_list = list(set(map(get_category, expenses)))
        def get_expenses_category_amount(category):
            amount = 0
            filtered_by_category = Expenses.objects.filter(category=category)
            for item in filtered_by_category:
                amount += item.amount
            return amount
        for x in expenses:
            for y in source_list:
                finalrep[y] = get_expenses_category_amount(y)
        return JsonResponse({'expense_category_data' : finalrep}, safe=False)



def export_csv(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; file-name=Expenses'+str(datetime.datetime.now())+'+csv'
    writer=csv.writer(response)
    writer.writerow(['Date', 'Category', 'Amount', 'Description'])
    expenses=Expenses.objects.filter(person=request.user)

    for expense in expenses:
        writer.writerow([expense.date, expense.category, expense.amount, expense.description])
    return response

def export_excel(request):
    response=HttpResponse(content_type = 'application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expenses'+str(datetime.datetime.now())+'.xls'
    wb=xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Expenses')
    row_num = 0
    font_style=xlwt.XFStyle()
    font_style.font.bold = True

    columns=['Date', 'Category', 'Amount', 'Description']

    # title wriing
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    rows=Expenses.objects.filter(person=request.user).values_list('date', 'category', 'amount', 'description')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)
    return response
    
def export_pdf(request):
    expenses=Expenses.objects.filter(person=request.user)
    template_path='expenses/export-pdf.html'
    context={
        'expenses' : expenses
    }
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="repost_exenses.pdf"'
    template=get_template(template_path)
    html=template.render(context)

    pisa_status=pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>"+html+"</pre>")
    return response

def sort_expenses_desc(request):
    if request.method=='POST':
        column=json.loads(request.body).get('column')
        expenses=Expenses.objects.filter(person=request.user).order_by(column)
        data=expenses.values()
        return JsonResponse(list(data), safe=False)


def sort_expenses_asc(request):
    if request.method=='POST':
        column=json.loads(request.body).get('column')
        expenses=Expenses.objects.filter(person=request.user).order_by('-'+column)
        data=expenses.values()
        return JsonResponse(list(data), safe=False)