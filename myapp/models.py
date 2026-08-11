from django.db import models
from myapp.models import *

class Service(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    short_description = models.TextField()
    description = models.TextField()
    icon = models.CharField(max_length=100, default="fa-solid fa-star")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.TextField(blank=True)
    badge = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_features(self):
        return [feature.strip() for feature in self.features.splitlines() if feature.strip()]

    def __str__(self):
        return self.name


class PricingPlan(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    badge = models.CharField(max_length=100, blank=True)
    short_description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=50, default="30 Mins")
    features = models.TextField(help_text="Enter each feature on a new line")
    is_popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_features(self):
        return [feature.strip() for feature in self.features.splitlines() if feature.strip()]

    def __str__(self):
        return self.name

class Appointment(models.Model):

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    LANGUAGE_CHOICES = [
        ("Hindi", "Hindi"),
        ("English", "English"),
        ("Punjabi", "Punjabi"),
    ]

    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="appointments")
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    time_of_birth = models.TimeField()
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    birth_place = models.CharField(max_length=200)
    consultation_date = models.DateField(null=True, blank=True)
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default="English")
    question = models.TextField(blank=True)
    plan = models.ForeignKey(PricingPlan, on_delete=models.PROTECT, related_name="appointments")
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return f"{self.full_name} - {self.service.name}"

class Payment(models.Model):
    STATUS_CHOICES = [("Pending", "Pending"), ("Success", "Success"), ("Failed", "Failed")]

    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="payment")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_id} - ₹{self.amount}"
