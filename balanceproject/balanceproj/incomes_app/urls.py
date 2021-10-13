from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name="incomes"

urlpatterns = [
    path('', views.index, name="index"),
    path('add-incomes', views.add_incomes, name="add_incomes"),
    path('edit-incomes/<int:id>', views.edit_incomes, name="edit_incomes"),
    path('del-incomes/<int:id>', views.del_incomes, name="del_incomes"),
    path('search-incomes', csrf_exempt(views.search_incomes), name="search_incomes"),
    path('stats-incomes', views.stats_incomes, name="stats_incomes"),
    path('income-summary', csrf_exempt(views.summary_incomes), name="summary_incomes"),
    path('export-csv', views.export_csv, name="export_csv"),
    path('export-excel', views.export_excel, name="export_excel"),
    path('export-pdf', views.export_pdf, name="export_pdf"),
    path('export-pdf', views.export_pdf, name="export_pdf"),
    path('sort-incomes-desc', csrf_exempt(views.sort_incomes_desc), name="sort_incomes_desc"),
    path('sort-incomes-asc', csrf_exempt(views.sort_incomes_asc), name="sort_incomes_asc"),
]