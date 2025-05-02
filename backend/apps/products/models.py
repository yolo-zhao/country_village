from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils.crypto import get_random_string

class Product(models.Model):
    """
    农特产品
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', '草稿'),
            ('published', '已发布'),
            ('sold_out', '已售罄'),
            ('unavailable', '已下架'),
        ],
        default='published'
    )

    class Meta:
        verbose_name = _("农特产品")
        verbose_name_plural = _("农特产品列表")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # 确保slug不为空
        if not self.slug and self.name:
            # 生成基础slug
            base_slug = slugify(self.name)
            if not base_slug:
                # 如果名称不能生成有效的slug（例如全中文名称），则使用随机字符串
                base_slug = 'product-' + get_random_string(8)
            
            # 检查是否已存在相同的slug
            existing_slugs = Product.objects.filter(slug__startswith=base_slug).values_list('slug', flat=True)
            if base_slug in existing_slugs:
                # 如果存在，添加随机后缀
                random_suffix = get_random_string(4)
                self.slug = f"{base_slug}-{random_suffix}"
            else:
                self.slug = base_slug
        
        super().save(*args, **kwargs)

class ProductImage(models.Model):
    """
    农特产品图片
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/images/')  # 保持原有的ImageField
    image_url = models.CharField(max_length=500, blank=True, null=True)  # 添加URL字段，支持外部URL
    caption = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = _("农特产品图片")
        verbose_name_plural = _("农特产品图片列表")

    def __str__(self):
        return self.caption or self.image.name
        
    def get_image_url(self):
        """返回图片URL，优先使用image_url字段"""
        if self.image_url:
            # 如果已经是完整URL，直接返回
            if self.image_url.startswith('http://') or self.image_url.startswith('https://'):
                return self.image_url
            # 否则添加域名
            return f"/media/{self.image_url}"
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return ""

class ProductInquiry(models.Model):
    """
    农特产品咨询
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inquiries')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='product_inquiries')
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100) # 可以是电话或邮箱
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    response = models.TextField(blank=True, null=True)
    responded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _("农特产品咨询")
        verbose_name_plural = _("农特产品咨询列表")

    def __str__(self):
        return f"{self.name} 咨询了 {self.product.name}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='用户')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"购物车 ({self.user if self.user else '未登录用户'})"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE, verbose_name='购物车')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, verbose_name='商品')
    quantity = models.PositiveIntegerField(default=1, verbose_name='数量')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '购物车商品项'
        verbose_name_plural = verbose_name
        unique_together = ('cart', 'product')  # 同一个购物车中，每个商品只能有一项

    def __str__(self):
        return f"{self.product.name} x {self.quantity} (在 {self.cart} 中)"

    def total_price(self):
        return self.product.price * self.quantity