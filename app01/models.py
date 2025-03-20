from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db import models

class Phone(models.Model):
    id = models.AutoField(primary_key=True, unique=True)  # 主键，Django 会自动创建
    name = models.CharField(max_length=100)  # 设备名称，限制最大长度100字符
    color = models.CharField(max_length=50)  # 颜色，最大50字符
    storage = models.IntegerField()  # 存储容量，单位GB
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 价格，支持两位小数
    stock = models.IntegerField(default=0)

class Tablet(models.Model):
    id = models.AutoField(primary_key=True, unique=True)  # 主键，Django 会自动创建
    name = models.CharField(max_length=100)  # 设备名称，限制最大长度100字符
    size = models.CharField(max_length=50)  # 尺寸，最大50字符
    color = models.CharField(max_length=50)  # 颜色，最大50字符
    storage = models.IntegerField()  # 存储容量，单位GB
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 价格，支持两位小数
    stock = models.IntegerField(default=0)

class Laptop(models.Model):
    id = models.AutoField(primary_key=True, unique=True)  # 主键，Django 会自动创建
    name = models.CharField(max_length=100)  # 设备名称，限制最大长度100字符
    size = models.CharField(max_length=50)  # 尺寸，最大50字符
    color = models.CharField(max_length=50)  # 颜色，最大50字符
    memory = models.IntegerField()  # 内存，单位GBory = models.IntegerField()  # 内存，单位GB
    storage = models.IntegerField()  # 存储容量，单位GB
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 价格，支持两位小数
    stock = models.IntegerField(default=0)

class Watch(models.Model):
    id = models.AutoField(primary_key=True, unique=True)  # 主键，Django 会自动创建
    name = models.CharField(max_length=100)  # 设备名称，限制最大长度100字符
    case_color = models.CharField(max_length=50)  # 表盘，最大50字符
    strap_color = models.CharField(max_length=50)  # 表带，最大50字符
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 价格，支持两位小数
    stock = models.IntegerField(default=0) 
#     bag_item_id = models.AutoField(primary_key=True)
#     user = models.ForeignKey('User', on_delete=models.CASCADE)  # 关联用户
#     phone = models.ForeignKey('Phone', on_delete=models.CASCADE)  # 关联手机商品
#     name = models.CharField(max_length=100)  # 商品名称
#     model = models.CharField(max_length=50)  # 型号
#     color = models.CharField(max_length=50)  # 颜色
#     storage = models.IntegerField()  # 存储容量
#     quantity = models.IntegerField(default=1)  # 数量,默认为1
#     price = models.DecimalField(max_digits=10, decimal_places=2)  # 单价
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)  # 总价
#     created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
#     updated_at = models.DateTimeField(auto_now=True)  # 更新时间

    def save(self, *args, **kwargs):
        # 保存时自动计算总价
        self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)

""" class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50, null=False)
    password = models.CharField(max_length=255, null=False)

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50, null=False)
    email = models.EmailField(unique=True, max_length=100, null=False)
    password = models.CharField(max_length=255, null=False)

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)

class ShoppingCart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart_item_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    order_date = models.DateTimeField(null=False)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=False)

class OrderDetail(models.Model):
    order_detail_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=False)
    comment = models.CharField(max_length=255, null=False)
    review_date = models.DateTimeField(null=False)

class Return(models.Model):
    return_id = models.AutoField(primary_key=True)
    order_detail = models.ForeignKey(OrderDetail, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    return_date = models.DateTimeField(null=False)
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=False)
    reason = models.CharField(max_length=255, null=False)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False) """

class UserPaymentInfo(models.Model):
    """用户支付和地址信息模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # 用于未登录用户的session_key
    session_key = models.CharField(max_length=100, null=True, blank=True)
    
    # 地址信息
    title = models.CharField(max_length=20, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100, blank=True, null=True)
    town_city = models.CharField(max_length=50)
    county = models.CharField(max_length=50, blank=True, null=True)
    postcode = models.CharField(max_length=20)
    country = models.CharField(max_length=50, default="United Kingdom")
    is_business_address = models.BooleanField(default=False)
    
    # 联系信息
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # 支付信息 - 注意: 在生产环境中应该安全地存储这些信息或使用支付处理服务
    card_number_last4 = models.CharField(max_length=4, blank=True, null=True)
    card_expiry = models.CharField(max_length=7, blank=True, null=True)
    
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.user:
            return f"{self.user.username}'s Payment Info"
        else:
            return f"Guest Payment Info {self.id}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category_images', blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='product_images', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class UserPaymentInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=20, blank=True)
    firstName = models.CharField(max_length=100, blank=True)
    surname = models.CharField(max_length=100, blank=True)
    addressLine1 = models.CharField(max_length=200, blank=True)
    addressLine2 = models.CharField(max_length=200, blank=True, null=True)
    townCity = models.CharField(max_length=100, blank=True)
    county = models.CharField(max_length=100, blank=True, null=True)
    postcode = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    cardNumberLast4 = models.CharField(max_length=4, blank=True)
    expiryDate = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.user:
            return f"Payment info for {self.user.username}"
        return f"Payment info for session {self.session_key}"

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    )
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=100, null=True, blank=True)
    shipping_name = models.CharField(max_length=200)
    shipping_address = models.TextField()
    shipping_phone = models.CharField(max_length=20)
    shipping_email = models.EmailField()
    payment_method = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.shipping_name}"
    
    class Meta:
        ordering = ['-created_at']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    product_image = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.quantity}x {self.product_name} in Order #{self.order.id}"
    
    @property
    def subtotal(self):
        return self.product_price * self.quantity

class OrderFeedback(models.Model):
    FEEDBACK_TYPES = (
        ('question', 'Question'),
        ('problem', 'Problem'),
        ('suggestion', 'Suggestion'),
    )
    
    order = models.ForeignKey(Order, related_name='feedback', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=100, null=True, blank=True)
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES, default='question')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    admin_response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Feedback #{self.id} for Order #{self.order.id}"
    
    class Meta:
        ordering = ['-created_at']

# 聊天消息模型，用于存储客服对话
class ChatMessage(models.Model):
    MESSAGE_TYPES = (
        ('user', 'User'),
        ('agent', 'Agent'),
        ('system', 'System'),
    )
    
    feedback = models.ForeignKey(OrderFeedback, related_name='messages', on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, related_name='chat_messages', on_delete=models.CASCADE)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.message_type.capitalize()} message for Order #{self.order.id}"
    
    class Meta:
        ordering = ['created_at']