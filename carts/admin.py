from django.contrib import admin

from carts.models import Cart


class CartTabAdmin(admin.TabularInline):
    model = Cart
    fields = (
        "product",
        "quantity",
    )
    search_fields = (
        "product",
        "quantity",
    )
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = [
        "user_display",
        "product_display",
        "quantity",
    ]
    list_filter = [
        "user",
        "product__name",
    ]

    def user_display(self, obj):
        if obj.user:
            return str(obj.user)
        return "Анонимный пользователь"

    def product_display(self, obj):
        return str(obj.product.name)

    user_display.short_description = "Пользователь"
    product_display.short_description = "Товар"
