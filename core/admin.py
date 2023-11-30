from django.contrib import admin
from core.models import FoodTruck


@admin.register(FoodTruck)
class FoodTruckAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "facility_type",
        "location_description",
        "address",
        "latitude",
        "longitude",
    )
    search_fields = ("name", "address")
    list_filter = ("facility_type",)
    ordering = ("name", "address")
    readonly_fields = ("id", "created_at", "updated_at")
    fieldsets = (
        ("Food Truck", {"fields": ("name", "address", "latitude", "longitude")}),
        ("Metadata", {"fields": ("id", "created_at", "updated_at")}),
    )
