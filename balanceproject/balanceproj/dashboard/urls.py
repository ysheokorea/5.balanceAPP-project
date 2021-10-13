from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = "dashboard"

urlpatterns = [
    path('', views.index, name="index"),
    path('progress-bar', csrf_exempt(views.progress_bar), name="progress_bar"),
    path('dashboard-incomes-summary', views.dashboard_incomes_summary, name="dashboard_incomes_summary"),
    path('dashboard-expenses-summary', views.dashboard_expenses_summary, name="dashboard_expenses_summary"),
]