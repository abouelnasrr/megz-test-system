"""
URL configuration for megz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shop import views
from shop.views import finalize_order, dashboard_login, dashboard
from shop.views import change_stock
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include


# from shop.views import dashboard
urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('<int:id>/',views.detail,name='detail'),
    # path('checkout/',views.checkout,name='checkout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/<int:quantity>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase_quantity/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('get_cart_count/', views.get_cart_count, name='get_cart_count'),
    path('spare/', views.spare, name='spare'),
    path("finalize_order/", views.finalize_order, name="finalize_order"),
    path('receipt/<int:order_id>/', views.receipt, name='receipt'),
    path('receipts/', views.receipts, name='receipts'),
    path("remove_from_cart/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart_total/", views.cart_total, name="cart_total"),
    path("coming_soon/", views.coming_soon, name="coming_soon"),
    path("dashboard_login/", dashboard_login, name="dashboard_login"),
    # path("add_admin_user/", add_admin_user, name="add_admin_user"),
    # # path('decrypt_password/', decrypt_password, name='decrypt_password'),
    # path('get_password/<int:user_id>/', get_plaintext_password, name='get_password'),
    # path('delete_admin_user/<int:user_id>/', delete_admin_user, name='delete_admin_user'),
    path('change-stock/', change_stock, name='change_stock'),
    # path("assign_colors/", assign_colors, name="assign_colors"),
    path('auth/', include('authenticationlogin.urls')),
    path('invt/', include('inventory.urls')),
    path('finc/', include('financial.urls')),
    path('opers/', include('operations.urls')),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
