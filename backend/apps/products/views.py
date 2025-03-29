from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, ProductImage, ProductInquiry
from .forms import ProductInquiryForm, CreateProductForm

def product_list(request):
    products = Product.objects.filter(status='published') # 只显示已发布的商品
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    inquiry_form = ProductInquiryForm()

    if request.method == 'POST':
        inquiry_form = ProductInquiryForm(request.POST)
        if inquiry_form.is_valid():
            inquiry = inquiry_form.save(commit=False)
            inquiry.product = product
            inquiry.user = request.user if request.user.is_authenticated else None
            inquiry.save()
            return redirect('products:product_detail', product_id=product.id) # 刷新页面或跳转到成功页面

    return render(request, 'products/product_detail.html', {'product': product, 'inquiry_form': inquiry_form})

@login_required
def farmer_product_list(request):
    products = Product.objects.filter(farmer=request.user)
    return render(request, 'products/farmer_product_list.html', {'products': products})

@login_required
def create_product(request):
    if not hasattr(request.user, 'farmerprofile'):
        return redirect('home') # 或者显示错误信息

    form = CreateProductForm()
    if request.method == 'POST':
        form = CreateProductForm(request.POST, request.FILES) # 注意：这里需要处理多张图片上传
        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = request.user
            product.save()
            # 处理上传的图片
            for image in request.FILES.getlist('images'): # 假设表单中图片字段名为 'images'
                ProductImage(product=product, image=image).save()
            return redirect('products:farmer_product_list')

    return render(request, 'products/create_product.html', {'form': form})