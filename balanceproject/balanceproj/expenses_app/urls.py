from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name="expenses"

urlpatterns = [
    path('', views.index, name="index"),
    path('add-expenses', views.add_expenses, name="add_expenses"),
    path('edit-expenses/<int:id>', views.edit_expenses, name="edit_expenses"),
    path('del-expenses/<int:id>', views.del_expenses, name="del_expenses"),
    path('search-expenses', csrf_exempt(views.search_expenses), name="search_expenses"),
    path('stats-expenses', views.stats_expenses, name="stats_expenses"),
    path('expense-summary', csrf_exempt(views.summary_expenses), name="summary_expenses"),
    path('export-csv', views.export_csv, name="export_csv"),
    path('export-excel', views.export_excel, name="export_excel"),
    path('export-pdf', views.export_pdf, name="export_pdf"),
    path('sort-expenses-desc', csrf_exempt(views.sort_expenses_desc), name="sort_expenses_desc"),
    path('sort-expenses-asc', csrf_exempt(views.sort_expenses_asc), name="sort_expenses_asc"),
]
