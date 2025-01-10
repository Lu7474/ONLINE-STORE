from django.contrib import admin

from .models import Category, Products


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name"]


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "quantity", "price"]
    search_fields = ["name", "description"]
    list_filter = ["quantity", "category"]
    fields = [
        "name",
        "category",
        "slug",
        "description",
        "image",
        "price",
        "quantity",
    ]
