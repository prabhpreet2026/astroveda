from django.contrib import admin
from myapp.models import *


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_active", "display_order")
    list_filter = ("is_active",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("display_order",)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "service",
        "phone",
        "consultation_date",
        "language",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "language",
        "service",
        "created_at",
    )

    search_fields = (
        "full_name",
        "phone",
        "birth_place",
    )

    readonly_fields = ("created_at",)

    ordering = ("-created_at",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("transaction_id", "appointment", "amount", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("transaction_id", "appointment__full_name")
    readonly_fields = ("transaction_id", "created_at")

@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "duration", "is_popular", "is_active", "display_order")
    list_filter = ("is_popular", "is_active")
    search_fields = ("name", "badge", "short_description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("display_order",)