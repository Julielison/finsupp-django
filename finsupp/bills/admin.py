from django.contrib import admin
from .models import Bill, BillItem

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ("id", "account", "total", "status", "due_date", "paid_date")

@admin.register(BillItem)
class BillItemAdmin(admin.ModelAdmin):
    list_display = ("id", "bill", "description", "amount")
