from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from .models import Source, Incomes
from django.contrib import messages

# Login
from django.contrib.auth.decorators import login_required

# json _ javascript
import json

# Paginator
from django.core.paginator import Paginator

# Date time
import datetime

# Export files
import csv
import xlwt
from django.template.loader import get_template
from xhtml2pdf import pisa


# Create your views here.
@login_required(login_url='authentication/login')
def index(request):
    sources=Source.objects.all()
    # At the beginnig query set for "Incomes" does not exists. 
    # Why doest not this alert error?
    incomes=Incomes.objects.filter(person=request.user)
    paginator = Paginator(incomes, 20)
    page_number = request.GET.get('page')
    page_obj=Paginator.get_page(paginator, page_number)
    context = {
         'sources' : sources,
         'incomes' : incomes,
         'page_obj' : page_obj,
         'range' : range(1,11),
    }
    return render(request, 'incomes/index.html', context)

def add_incomes(request):
    sources = Source.objects.all()
    context = {
        'sources' : sources,
        'values' : request.POST,
    }

    if request.method == 'GET':
        return render(request, 'incomes/add-incomes.html', context)


    if request.method == 'POST':
        date = request.POST['date']
        source = request.POST['source']
        amount = request.POST['amount']
        description = request.POST['description']

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'incomes/add-incomes.html', context)
        if not amount:
            messages.error(request, 'amount is required')
            return render(request, 'incomes/add-incomes.html', context)
        if not description:
            messages.error(request, 'description is required')
            return render(request, 'incomes/add-incomes.html', context)


    Incomes.objects.create(date=date, source=source,amount=amount,description=description,person=request.user)

    messages.success(request, 'Incomes saved successfully')
    return redirect('/incomes')
    
def edit_incomes(request, id):
    sources=Source.objects.all()
    incomes=Incomes.objects.get(pk=id)
    context={
        'incomes' : incomes,
        'sources' : sources,
        'values' : request.POST,
    }
    if request.method=='GET':
        return render(request, 'incomes/edit-incomes.html', context)
    if request.method=='POST':
        date = request.POST['date']
        source = request.POST['source']
        amount = request.POST['amount']
        description = request.POST['description']

        if not amount:
            messages.error(request, 'amount is required')
            return render(request, 'incomes.add-incomes.html', context)
        if not description:
            messages.error(request, 'description is required')
            return render(request, 'incomes.add-incomes.html', context)
    
    incomes.person = request.user
    if not date:
        incomes.date = incomes.date
    incomes.source = source
    incomes.amount = amount
    incomes.description = description
    incomes.save()

    messages.success(request, 'Incomes edit successfully')
    return redirect('/incomes')

def del_incomes(request, id):
    incomes=Incomes.objects.get(pk=id)
    incomes.delete()

    messages.success(request, 'Incomes successfully deleted')
    return redirect('/incomes')

def search_incomes(request):
    if request.method=='POST':
        search_str = json.loads(request.body).get('searchText')
    
        incomes = Incomes.objects.filter(
                amount__istartswith=search_str, person=request.user) | Incomes.objects.filter(
                date__istartswith=search_str, person=request.user) | Incomes.objects.filter(
                description__icontains=search_str, person=request.user) | Incomes.objects.filter(
                source__icontains=search_str, person=request.user)
        data = incomes.values()
        return JsonResponse(list(data), safe=False)

def stats_incomes(request):
    return render(request, 'incomes/stats-incomes.html')

def summary_incomes(request):
    if request.method == 'POST':
        year_val = json.loads(request.body).get('yearVal')
        month_val = json.loads(request.body).get('monthVal')

        todays_date = datetime.date.today()
        six_month_ago = todays_date - datetime.timedelta(days=30*6)
        # incomes = Incomes.objects.filter(person=request.user, date__gte=six_month_ago, date__lte=todays_date)
        incomes = Incomes.objects.filter(person=request.user, date__istartswith=(year_val+'-'+month_val))
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

    return redirect('/income-summary')

def export_csv(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; file-name=Incomes'+str(datetime.datetime.now())+'.csv'
    writer=csv.writer(response)
    writer.writerow(['Date','Source','Amount','Description'])
    incomes=Incomes.objects.filter(person=request.user)

    for income in incomes:
        writer.writerow([income.date, income.source, income.amount, income.description])
    return response

def export_excel(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Incomes'+str(datetime.datetime.now())+'.xls'
    wb=xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Incomes')
    row_num=0
    font_style=xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Date','Source','Amount','Description']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    rows=Incomes.objects.filter(person=request.user).values_list('date','source','amount','description')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)
    return response

def export_pdf(request):
    incomes=Incomes.objects.filter(person=request.user)
    template_path='incomes/export-pdf.html'
    context={'incomes' : incomes}
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html=template.render(context)

    pisa_status=pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>"+ html + '</pre>')
    return response


def sort_incomes_desc(request):
    if request.method=='POST':
        column=json.loads(request.body).get('column')
        incomes=Incomes.objects.filter(person=request.user).order_by(column)
        data=incomes.values()
        return JsonResponse(list(data), safe=False)


def sort_incomes_asc(request):
    if request.method=='POST':
        column=json.loads(request.body).get('column')
        incomes=Incomes.objects.filter(person=request.user).order_by('-'+column)
        data=incomes.values()
        return JsonResponse(list(data), safe=False)
    
