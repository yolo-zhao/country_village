from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, ProductImage, ProductInquiry,Cart,CartItem
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
#购物车的相关功能，添加，查看，删除
@login_required(login_url='/users/login/')  # 需要用户登录才能操作购物车
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('products:product_detail', product_id=product_id) # 假设您有商品详情页

@login_required(login_url='/users/login/')
def view_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = []
    if cart:
        cart_items = cart.items.all()
    context = {'cart_items': cart_items}
    return render(request, 'products/cart.html', context)

@login_required(login_url='/users/login/')
def update_cart_item(request, item_id):
    if request.method == 'POST':
        try:
            cart_item = CartItem.objects.get(pk=item_id, cart__user=request.user)
            quantity = int(request.POST.get('quantity', 1))
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete()
            return redirect('products:view_cart')
        except CartItem.DoesNotExist:
            # 处理购物车项不存在的情况
            pass
    return redirect('products:view_cart')

@login_required(login_url='/users/login/')
def remove_from_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(pk=item_id, cart__user=request.user)
        cart_item.delete()
    except CartItem.DoesNotExist:
        # 处理购物车项不存在的情况
        pass
    return redirect('products:view_cart')
@login_required(login_url='/users/login/')
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = []
    total_price = 0
    if cart:
        cart_items = cart.items.all()
        for item in cart_items:
            total_price += item.total_price()

    context = {'cart_items': cart_items, 'total_price': total_price}
    return render(request, 'products/checkout.html', context)