from django.contrib import admin
from .models import Product, ProductImage, ProductInquiry

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'farmer', 'status')
    list_filter = ('farmer', 'status')
    search_fields = ('name', 'description')
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductInquiry)