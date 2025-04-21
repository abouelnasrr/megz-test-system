from django.shortcuts import render, redirect
from .models import StockWarning
from .forms import StockWarningForm
from shop.models import Products
from django.contrib.auth.decorators import login_required

# @login_required
def inventory_view(request):
    form = StockWarningForm()
    stock_warnings = StockWarning.objects.all()
    products = Products.objects.all()

    red_alerts = []
    yellow_alerts = []

    for product in products:
        if product.stock == 0:
            red_alerts.append(product)
        else:
            warning = stock_warnings.filter(product=product).first()
            if warning and product.stock <= warning.warning_limit:
                yellow_alerts.append(product)

    if request.method == "POST":
        form = StockWarningForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inventory_page")

    context = {
        "form": form,
        "stock_warnings": stock_warnings,
        "products": products,
        "red_alerts": red_alerts,
        "yellow_alerts": yellow_alerts,
    }

    return render(request, "inventory/inventory.html", context)

# @login_required
def delete_warning(request, id):
    warning = StockWarning.objects.get(id=id)
    warning.delete()
    return redirect("inventory_page")
