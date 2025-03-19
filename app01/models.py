from django.db import models

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
# class BagItem(models.Model):
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