from shop.models import WebsiteLogo

def site_logo(request):
    logo = WebsiteLogo.objects.first()
    return {'logo': logo}
