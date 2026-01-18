from django.db import models

class AdminSettings(models.Model):
    monthly_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    yearly_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    sham_cash_account = models.CharField(max_length=255, default="Main Account")
    sham_cash_number = models.CharField(max_length=255, default="0900000000")

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Admin Settings (Singleton)"
