from django.contrib import admin
from .models import Category, Product, ProductImage

# Позволяет добавлять фото прямо внутри страницы товара
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # сколько пустых полей для фото выводить по умолчанию
    fields = ("image", "alt_text", "is_main")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)} # Автоматически заполняет slug из имени

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "old_price", "stock", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline] # Добавляем галерею в карточку товара