from django import forms
from .models import Product, ProductInquiry

class ProductInquiryForm(forms.ModelForm):
    class Meta:
        model = ProductInquiry
        fields = ['name', 'contact', 'message']

class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'status']
        # fields = ['name', 'description', 'price', 'stock', 'status', 'images'] # 注意：images字段需要特殊处理