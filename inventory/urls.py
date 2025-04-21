from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_view, name="inventory_page"),
    path('delete/<int:id>/', views.delete_warning, name='delete_warning'),


]
