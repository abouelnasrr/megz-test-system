from django.db import models
from django.utils.timezone import now, timedelta

class ChatMessage(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(default=now)

    def expires_at(self):
        return self.timestamp + timedelta(hours=24)

    def remaining_seconds(self):
        delta = self.expires_at() - now()
        return max(int(delta.total_seconds()), 0)

    def __str__(self):
        return f"Message at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

class Announcement(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.name} says: {self.message}"
