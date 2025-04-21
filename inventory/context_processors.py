from .models import StockWarning
from shop.models import Products

def inventory_alerts(request):
    red_alerts = []
    yellow_alerts = []

    for warning in StockWarning.objects.select_related("product"):
        product = warning.product
        if product.stock == 0:
            red_alerts.append(product)
        elif product.stock <= warning.warning_limit:
            yellow_alerts.append(product)

    color = "success"  # default green
    if red_alerts and yellow_alerts:
        color = "warning"
    if red_alerts:
        color = "danger"
    elif yellow_alerts:
        color = "warning"

    return {"inventory_alert_color": color}
