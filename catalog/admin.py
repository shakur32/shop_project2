from django.contrib import admin
from .models import Category, Product, ProductImage, Publication

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # Позволит добавлять сразу 3 фото

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline] # Это добавит блок с фото внутрь товара

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(ProductImage)
admin.site.register(Publication)