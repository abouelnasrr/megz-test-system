from django.urls import path
from . import views

urlpatterns = [
    path('', views.financial_page, name='financial_page'),
    path('expenses/', views.expenses_page, name='expenses_page'),
]
