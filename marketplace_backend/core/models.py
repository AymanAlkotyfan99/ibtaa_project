from django.db import models
from django.contrib.postgres.fields import ArrayField
import json

class AdminSettings(models.Model):
    monthly_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    yearly_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    sham_cash_account = models.CharField(max_length=255, default="Main Account")
    sham_cash_number = models.CharField(max_length=255, default="0900000000")
    subscription_plans = models.TextField(
        default='[{"name":"Basic","price":9.99,"duration_days":30,"max_products":10,"description":"Perfect for starters"},{"name":"Pro","price":29.99,"duration_days":30,"max_products":50,"description":"For growing businesses"},{"name":"Enterprise","price":99.99,"duration_days":30,"max_products":1000,"description":"For large scale operations"}]',
        help_text="JSON array of subscription plans"
    )

    def get_subscription_plans(self):
        """Parse subscription_plans JSON string to list"""
        try:
            if isinstance(self.subscription_plans, str):
                return json.loads(self.subscription_plans)
            return self.subscription_plans or []
        except (json.JSONDecodeError, TypeError):
            return []

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Admin Settings (Singleton)"
