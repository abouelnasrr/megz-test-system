from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .models import ChatMessage, Announcement
from django.utils.timezone import now

def operations_dashboard(request):
    now_time = now()
    messages = ChatMessage.objects.all()
    messages = [msg for msg in messages if msg.expires_at() > now_time]  # filter out expired
    announcements = Announcement.objects.order_by('-timestamp')
    return render(request, 'operations/operations_dashboard.html', {
        'messages': messages,
        'announcements': announcements,
    })

# Handles posting chat messages
def post_chat_message(request):
    if request.method == "POST":
        message = request.POST.get("message")
        if message:
            ChatMessage.objects.create(message=message, timestamp=now())
    return redirect('operations_dashboard')


# Handles posting announcements
def post_announcement(request):
    if request.method == "POST":
        name = request.POST.get("name")
        message = request.POST.get("message")
        if name and message:
            Announcement.objects.create(name=name, message=message, timestamp=now())
    return redirect('operations_dashboard')