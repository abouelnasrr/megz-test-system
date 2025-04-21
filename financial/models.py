from django.db import models
from django.utils.timezone import now

class Expense(models.Model):
    name = models.CharField(max_length=255)
    expense_type = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.name} - {self.amount} ({self.created_at.strftime('%Y-%m-%d')})"
