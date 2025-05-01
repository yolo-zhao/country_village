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
from rest_framework import viewsets, permissions, generics, filters
from rest_framework.views import APIView
from .models import Product, ProductImage, ProductInquiry, Cart, CartItem
from .serializers import ProductSerializer, ProductImageSerializer, ProductInquirySerializer, CartSerializer, CartItemSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from rest_framework.permissions import IsAuthenticated

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
    
    def list(self, request):
        # 获取用户的购物车，如果不存在则创建
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

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

# 添加缺少的视图类
class ProductSearchView(generics.ListAPIView):
    """
    产品搜索视图
    """
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'farmer__username']
    
    def get_queryset(self):
        queryset = Product.objects.filter(status='published')
        
        # 分类过滤
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        
        # 价格范围过滤
        min_price = self.request.query_params.get('min_price', None)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        max_price = self.request.query_params.get('max_price', None)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
            
        return queryset

class ProductRecommendationsView(APIView):
    """
    产品推荐视图
    """
    def get(self, request):
        # 获取热门产品（基于评价和订单数量）
        popular_products = Product.objects.filter(status='published').annotate(
            inquiry_count=Count('inquiries')
        ).order_by('-inquiry_count')[:5]
        
        # 返回推荐产品
        serializer = ProductSerializer(popular_products, many=True)
        return Response(serializer.data)

class ProductFavoritesView(APIView):
    """
    用户收藏产品视图
    """
    def get(self, request):
        # 这里假设有个 UserFavorite 模型用于保存用户收藏
        # 由于模型可能未定义，我们返回空列表作为示例
        return Response([])
    
    def post(self, request):
        # 添加收藏的逻辑
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({"error": "需要提供产品ID"}, status=400)
            
        try:
            product = Product.objects.get(id=product_id)
            # 假设有个 UserFavorite 模型，这里添加收藏
            # UserFavorite.objects.create(user=request.user, product=product)
            return Response({"message": "添加收藏成功"})
        except Product.DoesNotExist:
            return Response({"error": "产品不存在"}, status=404)
    
    def delete(self, request):
        # 取消收藏的逻辑
        product_id = request.query_params.get('product_id')
        if not product_id:
            return Response({"error": "需要提供产品ID"}, status=400)
            
        # 假设有个 UserFavorite 模型，这里删除收藏
        # UserFavorite.objects.filter(user=request.user, product_id=product_id).delete()
        return Response({"message": "取消收藏成功"})

class ProductCategoryView(APIView):
    """
    产品分类视图
    """
    def get(self, request):
        # 这里应该返回产品分类，但由于模型可能未定义，我们返回空列表作为示例
        categories = [
            {"id": 1, "name": "水果"},
            {"id": 2, "name": "蔬菜"},
            {"id": 3, "name": "谷物"},
            {"id": 4, "name": "肉类"},
            {"id": 5, "name": "乳制品"}
        ]
        return Response(categories)

class PopularProductsView(APIView):
    """
    热门产品视图
    """
    def get(self, request):
        # 获取热门产品（基于评价和订单数量）
        popular_products = Product.objects.filter(status='published').annotate(
            inquiry_count=Count('inquiries')
        ).order_by('-inquiry_count')[:10]
        
        # 返回热门产品
        serializer = ProductSerializer(popular_products, many=True)
        return Response(serializer.data)

class CartSingleView(APIView):
    """
    单个购物车视图 - 兼容前端'/cart/'路径
    """
    permission_classes = [permissions.IsAuthenticated]  # 只有登录用户才能操作购物车
    
    def get(self, request):
        # 获取或创建用户的购物车
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    def post(self, request):
        # 添加商品到购物车
        cart, created = Cart.objects.get_or_create(user=request.user)
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
        
    def delete(self, request):
        # 清空购物车
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart.items.all().delete()
            return Response({"message": "Cart cleared successfully"})
        return Response({"message": "No cart found"})

class CartAddItemView(APIView):
    """
    添加商品到购物车 - 兼容前端'/cart/add_item/'路径
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        # 获取或创建用户的购物车
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        if not product_id:
            return Response({'error': 'Product ID is required'}, status=400)
            
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)
            
        # 查找或创建购物车项
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity
            )
            
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class CartItemOperationView(APIView):
    """
    购物车项目操作 - 兼容前端'/cart/items/{id}/'路径
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, item_id):
        # 获取特定购物车项
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=404)
    
    def put(self, request, item_id):
        # 更新购物车项数量
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            quantity = int(request.data.get('quantity', 1))
            
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
                serializer = CartItemSerializer(cart_item)
                return Response(serializer.data)
            else:
                cart_item.delete()
                return Response({'message': 'Item removed from cart'})
                
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=404)
    
    def delete(self, request, item_id):
        # 从购物车中删除项目
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            cart_item.delete()
            return Response({'message': 'Item removed from cart'})
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=404)

class CartItemsView(APIView):
    """
    购物车项目批量操作 - 兼容前端'/cart/items/'路径
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # 获取用户购物车中的所有项目
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_items = cart.items.all()
            serializer = CartItemSerializer(cart_items, many=True)
            return Response(serializer.data)
        return Response([])
    
    def delete(self, request):
        # 清空购物车
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart.items.all().delete()
            return Response({'message': 'Cart cleared successfully'})
        return Response({'message': 'No cart found'})