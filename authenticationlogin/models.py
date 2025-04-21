from django.db import models
from django.utils import timezone

class AuthenticatedUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username

class LoginSession(models.Model):
    user = models.ForeignKey(AuthenticatedUser, on_delete=models.CASCADE)
    login_time = models.DateTimeField(default=timezone.now)
    logout_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.login_time} to {self.logout_time or 'Active'}"
