# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from .models import Product, ProductImage, ProductInquiry,Cart,CartItem
# from .forms import ProductInquiryForm, CreateProductForm
#
# def product_list(request):
#     products = Product.objects.filter(status='published') # 只显示已发布的商品
#     return render(request, 'products/product_list.html', {'products': products})
#
# def product_detail(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     inquiry_form = ProductInquiryForm()
#
#     if request.method == 'POST':
#         inquiry_form = ProductInquiryForm(request.POST)
#         if inquiry_form.is_valid():
#             inquiry = inquiry_form.save(commit=False)
#             inquiry.product = product
#             inquiry.user = request.user if request.user.is_authenticated else None
#             inquiry.save()
#             return redirect('products:product_detail', product_id=product.id) # 刷新页面或跳转到成功页面
#
#     return render(request, 'products/product_detail.html', {'product': product, 'inquiry_form': inquiry_form})
#
# @login_required
# def farmer_product_list(request):
#     products = Product.objects.filter(farmer=request.user)
#     return render(request, 'products/farmer_product_list.html', {'products': products})
#
# @login_required
# def create_product(request):
#     if not hasattr(request.user, 'farmerprofile'):
#         return redirect('home') # 或者显示错误信息
#
#     form = CreateProductForm()
#     if request.method == 'POST':
#         form = CreateProductForm(request.POST, request.FILES) # 注意：这里需要处理多张图片上传
#         if form.is_valid():
#             product = form.save(commit=False)
#             product.farmer = request.user
#             product.save()
#             # 处理上传的图片
#             for image in request.FILES.getlist('images'): # 假设表单中图片字段名为 'images'
#                 ProductImage(product=product, image=image).save()
#             return redirect('products:farmer_product_list')
#
#     return render(request, 'products/create_product.html', {'form': form})
# #购物车的相关功能，添加，查看，删除
# @login_required(login_url='/users/login/')  # 需要用户登录才能操作购物车
# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     cart, created = Cart.objects.get_or_create(user=request.user)
#     cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
#
#     if not item_created:
#         cart_item.quantity += 1
#         cart_item.save()
#
#     return redirect('products:product_detail', product_id=product_id) # 假设您有商品详情页
#
# @login_required(login_url='/users/login/')
# def view_cart(request):
#     cart = Cart.objects.filter(user=request.user).first()
#     cart_items = []
#     if cart:
#         cart_items = cart.items.all()
#     context = {'cart_items': cart_items}
#     return render(request, 'products/cart.html', context)
#
# @login_required(login_url='/users/login/')
# def update_cart_item(request, item_id):
#     if request.method == 'POST':
#         try:
#             cart_item = CartItem.objects.get(pk=item_id, cart__user=request.user)
#             quantity = int(request.POST.get('quantity', 1))
#             if quantity > 0:
#                 cart_item.quantity = quantity
#                 cart_item.save()
#             else:
#                 cart_item.delete()
#             return redirect('products:view_cart')
#         except CartItem.DoesNotExist:
#             # 处理购物车项不存在的情况
#             pass
#     return redirect('products:view_cart')
#
# @login_required(login_url='/users/login/')
# def remove_from_cart(request, item_id):
#     try:
#         cart_item = CartItem.objects.get(pk=item_id, cart__user=request.user)
#         cart_item.delete()
#     except CartItem.DoesNotExist:
#         # 处理购物车项不存在的情况
#         pass
#     return redirect('products:view_cart')
# @login_required(login_url='/users/login/')
# def checkout(request):
#     cart = Cart.objects.filter(user=request.user).first()
#     cart_items = []
#     total_price = 0
#     if cart:
#         cart_items = cart.items.all()
#         for item in cart_items:
#             total_price += item.total_price()
#
#     context = {'cart_items': cart_items, 'total_price': total_price}
#     return render(request, 'products/checkout.html', context)



# backend/apps/products/views.py
from rest_framework import viewsets, permissions, generics
from .models import Product, ProductImage, ProductInquiry, Cart, CartItem
from .serializers import ProductSerializer, ProductImageSerializer, ProductInquirySerializer, CartSerializer, CartItemSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)

    @action(detail=True, methods=['POST'])
    def upload_image(self, request, pk=None):
        product = self.get_object()
        serializer = ProductImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductInquiryViewSet(viewsets.ModelViewSet):
    queryset = ProductInquiry.objects.all()
    serializer_class = ProductInquirySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user if self.request.user.is_authenticated else None)

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated] # 只有登录用户才能操作购物车

    def get_queryset(self):
        # 每个用户只能看到自己的购物车
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['POST'])
    def add_item(self, request, pk=None):
        cart = self.get_object()
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=400)

        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity += int(quantity)
            cart_item.save()
        except CartItem.DoesNotExist:
            CartItem.objects.create(cart=cart, product=product, quantity=quantity)

        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=True, methods=['DELETE'], url_path='items/(?P<item_id>\d+)')
    def remove_item(self, request, pk=None, item_id=None):
        cart = self.get_object()
        try:
            item = CartItem.objects.get(pk=item_id, cart=cart)
            item.delete()
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found in cart'}, status=404)

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated] # 只有登录用户才能操作购物车项

    def get_queryset(self):
        # 每个用户只能看到自己购物车中的商品项
        return CartItem.objects.filter(cart__user=self.request.user)