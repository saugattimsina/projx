from django.contrib import admin
from .models import Order, UserActivePositions

# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["user", "order_id", "symbol", "trade_direction", "related_order"]
    list_filter = ["user", "symbol", "trade_direction", "related_order", "filled"]


@admin.register(UserActivePositions)
class UserActivePositionsAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "symbol",
        "entry_price",
        "mark_price",
        "liquidationPrice",
        "breakEvenPrice",
        "marginRatio",
        "margin",
        "margin_percentage",
        "pnl",
    ]
