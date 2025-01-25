from django.contrib import admin
from .models import User
from carts.admin import CartTabAdmin
# from orders.admin import OrderTabulareAdmin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "email",
    ]
    search_fields = [
        "username",
        "email",
    ]

    inlines = [CartTabAdmin]
    # inlines = [CartTabAdmin, OrderTabulareAdmin]
