from django.contrib import admin

from .models import ChatMessage, Announcement

admin.site.register(ChatMessage)
admin.site.register(Announcement)