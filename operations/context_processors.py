from .models import Announcement
from django.utils.timezone import now
from datetime import timedelta

def latest_announcement(request):
    one_hour_ago = now() - timedelta(hours=1)
    latest = Announcement.objects.filter(timestamp__gte=one_hour_ago).order_by('-timestamp').first()
    return {'latest_announcement': latest}
