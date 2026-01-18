from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        MERCHANT = "MERCHANT", "Merchant"
        CUSTOMER = "CUSTOMER", "Customer"

    username = None
    email = models.EmailField("email address", unique=True)
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.CUSTOMER)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def is_merchant(self):
        return self.role == self.Role.MERCHANT

    @property
    def is_customer(self):
        return self.role == self.Role.CUSTOMER

class MerchantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="merchant_profile")
    business_name = models.CharField(max_length=255)
    is_subscribed = models.BooleanField(default=False)
    # Add other fields as needed

    def __str__(self):
        return f"{self.business_name} ({self.user.email})"

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile")
    # Add other fields as needed

    def __str__(self):
        return self.user.email
