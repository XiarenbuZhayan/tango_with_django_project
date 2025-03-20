from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.templatetags.static import static
from .models import UserPaymentInfo, Order, OrderItem, OrderFeedback, ChatMessage
import re
import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone

# 新增: 导入创建反馈模型所需的依赖
from django.views.decorators.csrf import csrf_exempt

# 添加密码验证函数
def is_valid_password(password):
    # 检查密码长度是否至少为8位
    if len(password) < 8:
        return False
    
    # 检查密码是否同时包含字母和数字
    has_letter = False
    has_digit = False
    
    for char in password:
        if char.isalpha():
            has_letter = True
        elif char.isdigit():
            has_digit = True
    
    return has_letter and has_digit

# Create your views here.
def index(request):
    return HttpResponse("Welcome")

def homepage(request):
    return render(request, "homepage.html")

def phone(request):
    return render(request, "phone.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        
        # 检查是否已经提交了密码
        password = request.POST.get('password')
        
        if password:  # 如果提交了密码，进行完整的登录流程
            # 验证密码格式
            if not is_valid_password(password):
                return render(request, 'signin_password.html', {
                    'error_message': 'The password must be composed of more than 8 numbers and letters.',
                    'username': username
                })
                
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                return redirect('homepage')
            else:
                return render(request, 'signin_password.html', {
                    'error_message': 'Password is incorrect',
                    'username': username
                })
        else:  # 如果只提交了用户名，检查用户是否存在
            try:
                user = User.objects.get(username=username)
                # 用户存在，进入密码输入页面
                return render(request, 'signin_password.html', {'username': username})
            except User.DoesNotExist:
                # 用户不存在，显示错误信息
                return render(request, 'signin.html', {'error_message': 'User does not exist'})
    
    return render(request, 'signin.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            return render(request, 'signup.html', {'error_message': 'The passwords you entered do not match'})
        
        # 验证密码格式
        if not is_valid_password(password):
            return render(request, 'signup.html', {'error_message': 'The password must be composed of more than 8 numbers and letters.'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error_message': 'Username already exists'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error_message': 'Email already exists'})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        auth_login(request, user)
        return redirect('homepage')
    
    return render(request, 'signup.html')

def signout(request):
    auth_logout(request)
    return redirect('homepage')

def personal_info(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    return render(request, 'personal_info.html')

def my_orders(request):
    if request.method == 'POST':
        try:
            # 从POST请求中获取订单数据
            data = json.loads(request.body)
            
            # 获取购物车数据
            cart_items = request.session.get('cart_items', [])
            
            # 如果购物车为空，返回错误
            if not cart_items:
                return JsonResponse({'status': 'error', 'message': 'Your shopping cart is empty'})
            
            # 从session中获取payment_info
            payment_info_session = request.session.get('payment_info', {})
            
            # 保存用户支付信息到数据库
            if payment_info_session:
                try:
                    if request.user.is_authenticated:
                        # 如果用户已登录，更新或创建与用户关联的支付信息
                        payment_info, created = UserPaymentInfo.objects.update_or_create(
                            user=request.user,
                            defaults={
                                'title': payment_info_session.get('title', ''),
                                'firstName': payment_info_session.get('firstName', ''),
                                'surname': payment_info_session.get('surname', ''),
                                'addressLine1': payment_info_session.get('addressLine1', ''),
                                'addressLine2': payment_info_session.get('addressLine2', ''),
                                'townCity': payment_info_session.get('townCity', ''),
                                'county': payment_info_session.get('county', ''),
                                'postcode': payment_info_session.get('postcode', ''),
                                'email': payment_info_session.get('email', ''),
                                'phone': payment_info_session.get('phone', ''),
                                'cardNumberLast4': payment_info_session.get('cardNumberLast4', ''),
                                'expiryDate': payment_info_session.get('expiryDate', '')
                            }
                        )
                    else:
                        # 对于未登录用户，使用session_key
                        session_key = request.session.session_key
                        if not session_key:
                            request.session.create()
                            session_key = request.session.session_key
                        
                        payment_info, created = UserPaymentInfo.objects.update_or_create(
                            session_key=session_key,
                            defaults={
                                'title': payment_info_session.get('title', ''),
                                'firstName': payment_info_session.get('firstName', ''),
                                'surname': payment_info_session.get('surname', ''),
                                'addressLine1': payment_info_session.get('addressLine1', ''),
                                'addressLine2': payment_info_session.get('addressLine2', ''),
                                'townCity': payment_info_session.get('townCity', ''),
                                'county': payment_info_session.get('county', ''),
                                'postcode': payment_info_session.get('postcode', ''),
                                'email': payment_info_session.get('email', ''),
                                'phone': payment_info_session.get('phone', ''),
                                'cardNumberLast4': payment_info_session.get('cardNumberLast4', ''),
                                'expiryDate': payment_info_session.get('expiryDate', '')
                            }
                        )
                except Exception as e:
                    print(f"Error saving payment info to database: {e}")
            
            # 生成唯一的订单号 - 使用格式：年月日+随机数字
            import random
            order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
            
            # 创建订单记录
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key if not request.user.is_authenticated else None,
                shipping_name=data['shipping_address']['name'],
                shipping_address=f"{data['shipping_address']['address1']}, {data['shipping_address']['address2']}, {data['shipping_address']['city_postcode']}",
                shipping_phone=data['shipping_address']['phone'],
                shipping_email=data['shipping_address']['email'],
                # 确保payment_method不会太长，最多只保留95个字符
                payment_method=data['payment_method'][:95] if data['payment_method'] else 'Card payment',
                total_amount=data['total_amount'],
                status='Pending'
            )
            
            # 订单项总数量
            total_items = 0
            
            # 添加订单项
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product_name=item['name'],
                    product_price=item['price'],
                    quantity=item['quantity'],
                    product_image=item['image']
                )
                total_items += item['quantity']
            
            # 清空购物车
            request.session['cart_items'] = []
            request.session.modified = True
            
            # 将订单信息存储在session中，以便success页面使用
            request.session['last_order_id'] = order.id
            request.session['last_order_number'] = order_number  # 添加订单号
            request.session['last_order_date'] = order.created_at.strftime('%Y-%m-%d %H:%M:%S')
            request.session['last_order_total'] = str(order.total_amount)
            request.session['last_order_items'] = total_items  # 添加商品总数
            
            return JsonResponse({
                'status': 'success', 
                'message': 'Order placed successfully', 
                'order_id': order.id,
                'order_number': order_number
            })
        
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})
        except KeyError as e:
            return JsonResponse({'status': 'error', 'message': f'Missing required field: {str(e)}'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    # 处理GET请求 - 处理可能的订单操作，如取消订单
    if request.method == 'GET' and 'action' in request.GET and 'order_id' in request.GET:
        action = request.GET.get('action')
        order_id = request.GET.get('order_id')
        
        try:
            # 验证订单属于当前用户
            if request.user.is_authenticated:
                order = Order.objects.get(id=order_id, user=request.user)
            else:
                session_key = request.session.session_key
                order = Order.objects.get(id=order_id, session_key=session_key)
            
            if action == 'cancel':
                # 只有"Pending"和"Processing"状态的订单可以取消
                if order.status in ['Pending', 'Processing']:
                    order.status = 'Cancelled'
                    order.save()
                    messages.success(request, f'Order #{order.id} has been cancelled.')
                else:
                    messages.error(request, f'Cannot cancel order #{order.id} because it is already {order.status}.')
            
            # 可以添加其他可能的操作，如重新下单等
            
        except Order.DoesNotExist:
            messages.error(request, 'Order not found or you do not have permission to access it.')
    
    # 获取用户的订单
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
    else:
        session_key = request.session.session_key
        if not session_key:
            orders = []
        else:
            orders = Order.objects.filter(session_key=session_key).order_by('-created_at')
    
    # 为每个订单加载订单项和计算更多信息
    orders_with_items = []
    for order in orders:
        order_items = OrderItem.objects.filter(order=order)
        
        # 计算订单中的商品总数
        total_items = sum(item.quantity for item in order_items)
        
        # 获取订单状态的显示类
        status_class = get_status_class(order.status)
        
        # 确定可用的操作
        available_actions = []
        if order.status in ['Pending', 'Processing']:
            available_actions.append('cancel')
        
        orders_with_items.append({
            'order': order,
            'items': order_items,
            'total_items': total_items,
            'status_class': status_class,
            'available_actions': available_actions,
            'created_date': order.created_at.strftime('%Y-%m-%d'),
            'created_time': order.created_at.strftime('%H:%M:%S')
        })
    
    context = {
        'orders': orders_with_items,
        'orders_count': len(orders_with_items)
    }
    
    return render(request, 'my_orders.html', context)

# 帮助函数，获取订单状态的显示类
def get_status_class(status):
    status_classes = {
        'Pending': 'status-pending',
        'Processing': 'status-processing',
        'Shipped': 'status-shipped',
        'Delivered': 'status-delivered',
        'Cancelled': 'status-cancelled'
    }
    return status_classes.get(status, 'status-pending')

def success(request):
    """订单成功页面"""
    context = {}
    
    # 从session中获取最后一个订单的信息
    order_id = request.session.get('last_order_id')
    if order_id:
        context['order_id'] = order_id
        context['order_number'] = request.session.get('last_order_number')
        context['order_date'] = request.session.get('last_order_date')
        context['total_amount'] = request.session.get('last_order_total')
        context['order_items'] = request.session.get('last_order_items')
        
        # 清除session中的订单信息，避免刷新页面时重复显示
        # 但保留ID以便用户可以再次查看
        request.session.pop('last_order_number', None)
        request.session.pop('last_order_date', None)
        request.session.pop('last_order_total', None)
        request.session.pop('last_order_items', None)
    
    return render(request, 'success.html', context)

def bag(request):
    # 从session中获取购物车数据
    cart_items = request.session.get('cart_items', [])
    
    # 计算总价，考虑商品数量
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'items_count': len(cart_items)
    }
    
    return render(request, 'bag.html', context)

def add_to_bag(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            product_name = data.get('product_name')
            product_price = data.get('product_price')
            product_image = data.get('product_image')
            quantity = int(data.get('quantity', 1))
            update_quantity = data.get('update_quantity', False)
            
            # 获取当前购物车或创建新购物车
            cart_items = request.session.get('cart_items', [])
            
            # 如果是更新数量的请求
            if update_quantity:
                for item in cart_items:
                    if item['id'] == product_id:
                        item['quantity'] = quantity
                        break
            else:
                # 检查商品是否已在购物车中
                found = False
                for item in cart_items:
                    if item['id'] == product_id:
                        item['quantity'] += quantity
                        found = True
                        break
                
                # 如果商品不在购物车中，添加它
                if not found and product_price is not None:
                    product_price = float(product_price)
                    cart_items.append({
                        'id': product_id,
                        'name': product_name,
                        'price': product_price,
                        'image': product_image,
                        'quantity': quantity
                    })
            
            # 更新会话中的购物车
            request.session['cart_items'] = cart_items
            request.session.modified = True
            
            # 计算总价（包括数量）
            total_price = sum(item['price'] * item['quantity'] for item in cart_items)
            
            return JsonResponse({
                'success': True, 
                'message': 'Product added to bag',
                'items_count': len(cart_items),
                'total_price': total_price
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

def remove_from_bag(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            
            # 获取当前购物车
            cart_items = request.session.get('cart_items', [])
            
            # 移除指定商品
            cart_items = [item for item in cart_items if item['id'] != product_id]
            
            # 更新会话中的购物车
            request.session['cart_items'] = cart_items
            request.session.modified = True
            
            return JsonResponse({
                'success': True, 
                'message': 'Product removed from bag',
                'items_count': len(cart_items)
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

def phone_detail(request, phone_id):
    # 添加重定向逻辑
    if phone_id == 31:
        return redirect('iphone16pro')
    elif phone_id == 1:
        return redirect('iphone16')
    
    # 对于其他所有phone_id，直接返回404
    return HttpResponseNotFound("Phone not found")

def tablet(request):
    """
    View function for displaying tablet page
    """
    return render(request, 'tablet.html')

def laptop(request):
    return render(request, 'laptop.html')

def watch(request):
    """
    View function for displaying watch page
    """
    return render(request, 'watch.html')

def watch_se(request):
    """
    View function for displaying Apple Watch SE detail page
    """
    # Apple Watch SE数据
    watch_data = {
        'name': 'Apple Watch SE',
        'price': 219,
        'monthly_price': 10.38,
        'cases': [
            {'name': 'Midnight', 'hex_code': '#171e2b'},
            {'name': 'Starlight', 'hex_code': '#e9d7c7'},
            {'name': 'Silver', 'hex_code': '#d1d5db'},
        ],
        'straps': [
            {'name': 'Solo Loop - Northern Lights', 'hex_code': '#aef69c'},
            {'name': 'Solo Loop - Periwinkle', 'hex_code': '#7683b9'},
            {'name': 'Solo Loop - Peony', 'hex_code': '#f47da1'},
        ],
        'features': [
            '44mm or 40mm aluminum case',
            'Retina display (Up to 1,000 nits)',
            'S8 SiP processor',
            'High and low heart rate notifications',
            'Emergency SOS',
            'Crash Detection',
            'Water resistant 50 meters'
        ],
        'base_image': 'images/watch_se'
    }
    
    return render(request, 'watch_se.html', {'watch': watch_data})

def watch_series_10(request):
    """
    View function for displaying Apple Watch Series 10 detail page
    """
    # Apple Watch Series 10数据
    watch_data = {
        'name': 'Apple Watch Series 10',
        'price': 399,
        'monthly_price': 16.63,
        'cases': [
            {'name': 'Silver', 'hex_code': '#d1d5db'},
            {'name': 'Rose Gold', 'hex_code': '#e9c7c7'},
            {'name': 'Jet Black', 'hex_code': '#1a1a1a'}
        ],
        'straps': [
            {'name': 'Solo Loop - Northern Lights', 'hex_code': '#aef69c'},
            {'name': 'Solo Loop - Periwinkle', 'hex_code': '#7683b9'},
            {'name': 'Solo Loop - Peony', 'hex_code': '#f47da1'},
        ],
        'features': [
            '46mm or 42mm aluminum or titanium case',
            'Always-On Retina display (Up to 2,000 nits)',
            'S10 SiP processor',
            'ECG app and Blood Oxygen app',
            'High and low heart rate notifications',
            'Temperature sensing',
            'Crash Detection and Fall Detection',
            'Water resistant 50 meters'
        ],
        'base_image': 'images/watch_series_10'
    }
    
    return render(request, 'watch_series_10.html', {'watch': watch_data})

def watch_ultra_2(request):
    """
    View function for displaying Apple Watch Ultra 2 detail page
    """
    # Apple Watch Ultra 2数据
    watch_data = {
        'name': 'Apple Watch Ultra 2',
        'price': 799,
        'monthly_price': 33.29,
        'cases': [
            {'name': 'Natural Titanium', 'hex_code': '#dbd3c8'},
            {'name': 'Black Titanium', 'hex_code': '#2c2c2e'}
        ],
        'straps': [
            {'name': 'Alpine Loop - Tan', 'hex_code': '#C19A6B'},
            {'name': 'Alpine Loop - Navy', 'hex_code': '#2B2D42'},
            {'name': 'Alpine Loop - Dark Gray', 'hex_code': '#3A4A3F'}
        ],
        'features': [
            '49mm titanium case',
            'Always-On Retina display (Up to 3,000 nits)',
            'S9 SiP processor',
            'ECG app and Blood Oxygen app',
            'Temperature sensing',
            'Depth gauge and water temperature sensor',
            'Customizable Action button',
            'Up to 36 hours of battery life',
            'Water resistant 100 meters'
        ],
        'base_image': 'images/watch_ultra_2'
    }
    
    return render(request, 'watch_ultra_2.html', {'watch': watch_data})

def accessory(request):
    """
    View function for displaying accessory page
    """
    return render(request, 'accessory.html')

def airtag(request):
    return render(request, 'airtag.html')

def magsafe_charger(request):
    return render(request, 'magsafe_charger.html')
    
def apple_pencil(request):
    return render(request, 'apple_pencil.html')

def iphone_cases(request):
    return render(request, 'iphone_cases.html')

def magic_mouse(request):
    return render(request, 'magic_mouse.html')
    
def magic_keyboard(request):
    return render(request, 'magic_keyboard.html')

def homepod_mini(request):
    return render(request, 'homepod_mini.html')

def airpods_pro(request):
    return render(request, 'airpods_pro.html')

def iphone16(request):
    """
    View function for displaying iPhone 16 detail page
    """
    # iPhone 16数据
    phone = {
        'name': 'iPhone 16',
        'models': [
            {
                'name': 'iPhone 16',
                'display_size': '6.1-inch display',
                'price': 799,
                'storage_options': [
                    {'size': 128, 'price': 799},
                    {'size': 256, 'price': 899},
                    {'size': 512, 'price': 1099}
                ]
            },
            {
                'name': 'iPhone 16 Plus',
                'display_size': '6.7-inch display',
                'price': 899,
                'storage_options': [
                    {'size': 128, 'price': 899},
                    {'size': 256, 'price': 999},
                    {'size': 512, 'price': 1199}
                ]
            }
        ],
        'colors': [
            {'name': 'Ultramarine', 'hex_code': '#4B6CB7'},
            {'name': 'Teal', 'hex_code': '#367588'},
            {'name': 'Pink', 'hex_code': '#FAB4C1'},
            {'name': 'White', 'hex_code': '#F5F5F7'},
            {'name': 'Black', 'hex_code': '#1D1D1F'}
        ],
        'storage_options': [
            {'size': 128, 'price': 799},
            {'size': 256, 'price': 899},
            {'size': 512, 'price': 1099}
        ],
        'price': 799,
        'monthly_price': 33.29,
        'image': 'images/iphone_16__c5bvots96jee_xlarge_2x.png'
    }
    
    return render(request, 'iphone16.html', {'phone': phone})

def iphone16pro(request):
    """
    View function for displaying iPhone 16 Pro detail page
    """
    # 直接使用phone_id=31的数据
    phones = {
        31: {  # iPhone 16 Pro
            'name': 'iPhone 16 Pro',
            'models': [
                {
                    'name': 'iPhone 16 Pro',
                    'display_size': '6.1-inch display',
                    'price': 1099,
                    'storage_options': [
                        {'size': 256, 'price': 1099},
                        {'size': 512, 'price': 1299},
                        {'size': '1TB', 'price': 1499}
                    ]
                },
                {
                    'name': 'iPhone 16 Pro Max',
                    'display_size': '6.7-inch display',
                    'price': 1199,
                    'storage_options': [
                        {'size': 256, 'price': 1199},
                        {'size': 512, 'price': 1399},
                        {'size': '1TB', 'price': 1599}
                    ]
                }
            ],
            'colors': [
                {'name': 'Desert Titanium', 'hex_code': '#C1B6A5'},
                {'name': 'Natural Titanium', 'hex_code': '#E3D0B8'},
                {'name': 'White Titanium', 'hex_code': '#F5F5F7'},
                {'name': 'Black Titanium', 'hex_code': '#4C4C4C'}
            ],
            'storage_options': [
                {'size': 256, 'price': 1099},
                {'size': 512, 'price': 1299},
                {'size': '1TB', 'price': 1499}
            ],
            'price': 1099,
            'monthly_price': 45.79,
            'image': 'images/iphone_16pro__erw9alves2qa_xlarge_2x.png'
        }
    }
    
    phone = phones[31]
    return render(request, 'iphone16pro.html', {'phone': phone})

def ipadpro(request):
    tablet_data = {
        'name': 'iPad Pro',
        'price': 999,
        'monthly_price': 41.62,
        'display_size': '11-inch',
        'image': 'images/ipad_pro_silver.png',
        'models': [
            {'id': 1, 'name': 'iPad Pro 11-inch', 'price': 999, 'base_price': 999, 'display_size': '11-inch'},
            {'id': 2, 'name': 'iPad Pro 13-inch', 'price': 1299, 'base_price': 1299, 'display_size': '13-inch'}
        ],
        'colors': [
            {'name': 'Silver', 'hex_code': '#E3E3E3'},
            {'name': 'Space Black', 'hex_code': '#535150'}
        ],
        'storage_options': [
            {'size': 128, 'price': 999},
            {'size': 256, 'price': 1199},
            {'size': 512, 'price': 1399},
            {'size': 1024, 'price': 1799}
        ]
    }
    
    # 为13英寸型号准备不同的存储价格
    if 'model' in request.GET and request.GET.get('model') == '13-inch':
        tablet_data['name'] = 'iPad Pro 13-inch'
        tablet_data['price'] = 1299
        tablet_data['monthly_price'] = 54.12
        tablet_data['storage_options'] = [
            {'size': 128, 'price': 1299},
            {'size': 256, 'price': 1499},
            {'size': 512, 'price': 1699},
            {'size': 1024, 'price': 2099}
        ]
    
    return render(request, 'ipadpro.html', {'tablet': tablet_data})

def ipadair(request):
    tablet_data = {
        'name': 'iPad Air',
        'price': 599,
        'monthly_price': 24.96,
        'display_size': '11-inch',
        'image': 'images/ipad_air_blue.png',
        'models': [
            {'id': 1, 'name': 'iPad Air 11-inch', 'price': 599, 'base_price': 599, 'display_size': '11-inch'},
            {'id': 2, 'name': 'iPad Air 13-inch', 'price': 799, 'base_price': 799, 'display_size': '13-inch'}
        ],
        'colors': [
            {'name': 'Space Gray', 'hex_code': '#535150'},
            {'name': 'Blue', 'hex_code': '#557FA3'},
            {'name': 'Purple', 'hex_code': '#9A6EB5'},
            {'name': 'Starlight', 'hex_code': '#F0E4D3'}
        ],
        'storage_options': [
            {'size': 64, 'price': 599},
            {'size': 256, 'price': 699},
            {'size': 512, 'price': 899},
            {'size': 1024, 'price': 1099}
        ]
    }
    
    # 为13英寸型号准备不同的存储价格
    if 'model' in request.GET and request.GET.get('model') == '13-inch':
        tablet_data['name'] = 'iPad Air 13-inch'
        tablet_data['price'] = 799
        tablet_data['monthly_price'] = 33.29
        tablet_data['storage_options'] = [
            {'size': 64, 'price': 799},
            {'size': 256, 'price': 899},
            {'size': 512, 'price': 1099},
            {'size': 1024, 'price': 1299}
        ]
    
    return render(request, 'ipadair.html', {'tablet': tablet_data})

def ipad(request):
    tablet_data = {
        'name': 'iPad',
        'price': 329,
        'monthly_price': 13.71,
        'display_size': '10.9-inch',
        'image': 'images/ipad_blue.png',
        'colors': [
            {'name': 'Silver', 'hex_code': '#E3E3E3'},
            {'name': 'Blue', 'hex_code': '#557FA3'},
            {'name': 'Pink', 'hex_code': '#DE7C80'},
            {'name': 'Yellow', 'hex_code': '#FDDE55'}
        ],
        'storage_options': [
            {'size': 128, 'price': 329},
            {'size': 256, 'price': 429},
            {'size': 512, 'price': 629}
        ]
    }
    
    return render(request, 'ipad.html', {'tablet': tablet_data})

def ipadmini(request):
    tablet_data = {
        'name': 'iPad mini',
        'price': 499,
        'monthly_price': 20.79,
        'display_size': '8.3-inch',
        'image': 'images/ipad_mini_starlight.png',
        'colors': [
            {'name': 'Space Grey', 'hex_code': '#535150'},
            {'name': 'Blue', 'hex_code': '#557FA3'},
            {'name': 'Purple', 'hex_code': '#9A6EB5'},
            {'name': 'Starlight', 'hex_code': '#F0E4D3'}
        ],
        'storage_options': [
            {'size': 128, 'price': 499},
            {'size': 256, 'price': 599},
            {'size': 512, 'price': 799}
        ]
    }
    
    return render(request, 'ipadmini.html', {'tablet': tablet_data})

def macbookpro16(request):
    laptop = {
        'name': 'MacBook Pro 16"',
        'size': '16-inch',
        'price': 5199,
        'monthly_price': 216.62,
        'image': 'images/macbook_pro_16.png',
        'colors': [
            {'name': 'Space Black', 'hex_code': '#1D1D1F'},
            {'name': 'Silver', 'hex_code': '#F5F5F7'}
        ],
        'memory_options': [
            {'size': 64, 'price': 0},
            {'size': 128, 'price': 800}
        ],
        'storage_options': [
            {'size': '4TB', 'price': 0},
            {'size': '8TB', 'price': 1200}
        ]
    }
    return render(request, 'macbookpro16.html', {'laptop': laptop})

def macbookpro14(request):
    laptop_data = {
        'name': 'MacBook Pro 14"',
        'size': '14-inch',
        'price': 1999,
        'monthly_price': 83.29,
        'image': 'images/macbookpro14.png',
        'colors': [
            {'name': 'Space Black', 'hex_code': '#1d1d1f'},
            {'name': 'Silver', 'hex_code': '#e3e3e1'},
        ],
        'memory_options': [
            {'size': 16, 'price': 1999, 'price_diff': 0},
            {'size': 24, 'price': 2199, 'price_diff': 200},
            {'size': 32, 'price': 2399, 'price_diff': 400},
        ],
        'storage_options': [
            {'size': '1TB', 'price': 1999, 'price_diff': 0},
            {'size': '2TB', 'price': 2399, 'price_diff': 400},
        ],
    }
    return render(request, 'macbookpro14.html', {'laptop': laptop_data})

def macbookair13(request):
    laptop_data = {
        'name': 'MacBook Air 13"',
        'size': '13.6-inch',
        'price': 1199,
        'monthly_price': 49.96,
        'image': 'images/macbookair13.png',
        'colors': [
            {'name': 'Midnight', 'hex_code': '#1d1d1f'},
            {'name': 'Sky Blue', 'hex_code': '#64a9d9'},
        ],
        'memory_options': [
            {'size': 8, 'price': 1199, 'price_diff': 0},
            {'size': 16, 'price': 1399, 'price_diff': 200},
            {'size': 24, 'price': 1599, 'price_diff': 400},
        ],
        'storage_options': [
            {'size': 512, 'price': 1199, 'price_diff': 0},
            {'size': '1TB', 'price': 1499, 'price_diff': 200},
            {'size': '2TB', 'price': 1999, 'price_diff': 400},
        ],
    }
    return render(request, 'macbookair13.html', {'laptop': laptop_data})

def macbookair15(request):
    laptop_data = {
        'name': 'MacBook Air 15"',
        'size': '15.3-inch',
        'price': 1399,
        'monthly_price': 58.29,
        'image': 'images/macbookair15.png',
        'colors': [
            {'name': 'Midnight', 'hex_code': '#1d1d1f'},
            {'name': 'Sky Blue', 'hex_code': '#64a9d9'},
        ],
        'memory_options': [
            {'size': 16, 'price': 1399, 'price_diff': 0},
            {'size': 24, 'price': 1599, 'price_diff': 200},
            {'size': 32, 'price': 1799, 'price_diff': 400},
        ],
        'storage_options': [
            {'size': 512, 'price': 1399, 'price_diff': 0},
            {'size': '1TB', 'price': 1599, 'price_diff': 200},
            {'size': '2TB', 'price': 1999, 'price_diff': 600},
        ],
    }
    return render(request, 'macbookair15.html', {'laptop': laptop_data})

def payment_check(request):
    # 从session中获取购物车数据
    cart_items = request.session.get('cart_items', [])
    total_price = sum(float(item.get('price', 0)) * int(item.get('quantity', 1)) for item in cart_items)
    
    # 尝试获取用户的默认支付信息
    payment_info = None
    try:
        if request.user.is_authenticated:
            # 如果用户已登录，尝试获取与用户关联的支付信息
            payment_info = UserPaymentInfo.objects.filter(user=request.user).first()
        else:
            # 对于未登录用户，使用session_key作为标识
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            payment_info = UserPaymentInfo.objects.filter(session_key=session_key).first()
    except Exception as e:
        print(f"Error retrieving payment info: {e}")
    
    # 处理POST请求 - 保存支付信息到session，但不保存到数据库
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # 处理卡号 - 移除所有空格并获取最后4位
            card_number = data.get('cardNumber', '')
            if card_number:
                # 使用正则表达式替换所有空格
                card_number = re.sub(r'\s+', '', card_number)
                card_last_4 = card_number[-4:] if len(card_number) >= 4 else card_number
            else:
                card_last_4 = ''
            
            # 仅将支付信息存储在session中，以便checkout页面使用
            # 不再保存到数据库，而是在下单时再保存
            payment_info_dict = {
                'title': data.get('title', ''),
                'firstName': data.get('firstName', ''),
                'surname': data.get('surname', ''),
                'addressLine1': data.get('addressLine1', ''),
                'addressLine2': data.get('addressLine2', ''),
                'townCity': data.get('townCity', ''),
                'county': data.get('county', ''),
                'postcode': data.get('postcode', ''),
                'email': data.get('email', ''),
                'phone': data.get('phone', ''),
                'cardNumberLast4': card_last_4,
                'expiryDate': data.get('expiryDate', '')
            }
            
            # 将支付信息存储在session中
            request.session['payment_info'] = payment_info_dict
            
            # 注释掉原数据库保存代码
            """
            # 为用户或会话保存/更新支付信息
            if request.user.is_authenticated:
                payment_info, created = UserPaymentInfo.objects.update_or_create(
                    user=request.user,
                    defaults={
                        'title': data.get('title', ''),
                        'firstName': data.get('firstName', ''),
                        'surname': data.get('surname', ''),
                        'addressLine1': data.get('addressLine1', ''),
                        'addressLine2': data.get('addressLine2', ''),
                        'townCity': data.get('townCity', ''),
                        'county': data.get('county', ''),
                        'postcode': data.get('postcode', ''),
                        'email': data.get('email', ''),
                        'phone': data.get('phone', ''),
                        'cardNumberLast4': card_last_4,
                        'expiryDate': data.get('expiryDate', '')
                    }
                )
            else:
                session_key = request.session.session_key
                if not session_key:
                    request.session.create()
                    session_key = request.session.session_key
                
                payment_info, created = UserPaymentInfo.objects.update_or_create(
                    session_key=session_key,
                    defaults={
                        'title': data.get('title', ''),
                        'firstName': data.get('firstName', ''),
                        'surname': data.get('surname', ''),
                        'addressLine1': data.get('addressLine1', ''),
                        'addressLine2': data.get('addressLine2', ''),
                        'townCity': data.get('townCity', ''),
                        'county': data.get('county', ''),
                        'postcode': data.get('postcode', ''),
                        'email': data.get('email', ''),
                        'phone': data.get('phone', ''),
                        'cardNumberLast4': card_last_4,
                        'expiryDate': data.get('expiryDate', '')
                    }
                )
            """
            
            return JsonResponse({'status': 'success', 'message': 'Payment information saved successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    # 准备上下文数据
    context = {
        'total_price': total_price,
        'shopping_cart': cart_items
    }
    
    # 如果有支付信息，添加到上下文中
    if payment_info:
        context['payment_info'] = {
            'title': payment_info.title,
            'firstName': payment_info.firstName,
            'surname': payment_info.surname,
            'addressLine1': payment_info.addressLine1,
            'addressLine2': payment_info.addressLine2,
            'townCity': payment_info.townCity,
            'county': payment_info.county,
            'postcode': payment_info.postcode,
            'email': payment_info.email,
            'phone': payment_info.phone,
            'cardNumberLast4': payment_info.cardNumberLast4,
            'expiryDate': payment_info.expiryDate
        }
        
        # 将支付信息存储在session中，以便checkout页面使用
        request.session['payment_info'] = context['payment_info']
    
    return render(request, 'payment_check.html', context)

def checkout(request):
    # 从session中获取购物车和支付信息
    cart_items = request.session.get('cart_items', [])
    payment_info = request.session.get('payment_info', None)
    
    # 计算总价
    total_price = sum(float(item.get('price', 0)) * int(item.get('quantity', 1)) for item in cart_items)
    
    context = {
        'shopping_cart': cart_items,
        'payment_info': payment_info,
        'total_price': total_price
    }
    
    return render(request, 'checkout.html', context)

def change_info(request):
    """变更信息页面 - 返回到购物袋页面"""
    return redirect('bag')

# 处理订单反馈提交的视图函数
@csrf_exempt
def order_feedback(request):
    """Handle user order feedback submission"""
    if request.method == 'POST':
        try:
            # Parse request data
            data = json.loads(request.body)
            order_id = data.get('order_id')
            feedback_type = data.get('feedback_type')
            subject = data.get('subject')
            message = data.get('message')
            
            # Validate required fields
            if not all([order_id, feedback_type, subject, message]):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Please fill in all required fields'
                })
            
            # Find order
            try:
                order = Order.objects.get(id=order_id)
                
                # Create feedback
                feedback = OrderFeedback.objects.create(
                    order=order,
                    user=request.user if request.user.is_authenticated else None,
                    feedback_type=feedback_type,
                    subject=subject,
                    message=message
                )
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Feedback submitted successfully, we will reply soon'
                })
            except Order.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Order not found'
                })
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({
                'status': 'error',
                'message': f'Submission failed: {str(e)}'
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Method not supported'
    })

@login_required
def order_feedback_history(request, order_id):
    """Get feedback history for a specific order"""
    try:
        feedbacks = OrderFeedback.objects.filter(order_id=order_id).order_by('-created_at')
        feedback_list = []
        
        for feedback in feedbacks:
            feedback_list.append({
                'id': feedback.id,
                'feedback_type': feedback.get_feedback_type_display(),
                'subject': feedback.subject,
                'message': feedback.message,
                'admin_response': feedback.admin_response,
                'is_resolved': feedback.is_resolved,
                'created_at': feedback.created_at.strftime('%Y-%m-%d %H:%M')
            })
        
        return JsonResponse({
            'status': 'success',
            'feedbacks': feedback_list
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'status': 'error', 'message': str(e)})

@staff_member_required
def admin_feedback_list(request):
    """Admin view for all feedback"""
    feedbacks = OrderFeedback.objects.all().order_by('-created_at')
    return render(request, 'admin/order_feedbacks.html', {'feedbacks': feedbacks})

@staff_member_required
def admin_feedback_response(request):
    """Admin response to feedback"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            feedback_id = data.get('feedback_id')
            response = data.get('response')
            
            if not all([feedback_id, response]):
                return JsonResponse({'status': 'error', 'message': 'Missing required fields'})
            
            feedback = OrderFeedback.objects.get(id=feedback_id)
            feedback.admin_response = response
            feedback.save()
            
            return JsonResponse({'status': 'success', 'message': 'Response sent successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Failed to send response: {str(e)}'})
    
    return JsonResponse({'status': 'error', 'message': 'Method not supported'})

@staff_member_required
def admin_feedback_resolve(request):
    """Mark feedback as resolved"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            feedback_id = data.get('feedback_id')
            
            feedback = OrderFeedback.objects.get(id=feedback_id)
            feedback.is_resolved = True
            feedback.save()
            
            return JsonResponse({'status': 'success', 'message': 'Marked as resolved'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Operation failed: {str(e)}'})
    
    return JsonResponse({'status': 'error', 'message': 'Method not supported'})

# Admin panel views
@login_required
def admin_login(request):
    """
    View function for admin login.
    Only allows staff users to access the admin panel.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None and user.is_staff:
            auth_login(request, user)
            return redirect('admin_dashboard')
        else:
            if user is not None and not user.is_staff:
                error_message = '您不是管理员用户，无法访问管理后台'
            else:
                error_message = '用户名或密码错误'
            
            return render(request, 'admin/login.html', {'error_message': error_message})
    
    return render(request, 'admin/login.html')

@login_required
def admin_logout(request):
    """
    View function for admin logout.
    """
    if request.method == 'POST':
        auth_logout(request)
        return redirect('admin_login')
    return redirect('admin_dashboard')

@login_required
@staff_member_required
def admin_dashboard(request):
    """
    View function for the admin dashboard.
    Displays three main features: order search, real-time chat, and user message inquiries.
    """
    # Get all orders
    orders = Order.objects.all().order_by('-created_at')
    
    # Get active chats (feedbacks with at least one message in the last 24 hours)
    yesterday = timezone.now() - timezone.timedelta(days=1)
    active_chats = OrderFeedback.objects.filter(
        models.Q(messages__created_at__gte=yesterday) | 
        models.Q(created_at__gte=yesterday)
    ).distinct().order_by('-messages__created_at')
    
    # Get all order feedbacks
    order_feedbacks = OrderFeedback.objects.all().order_by('-created_at')
    
    context = {
        'orders': orders,
        'active_chats': active_chats,
        'order_feedbacks': order_feedbacks,
    }
    
    return render(request, 'admin/dashboard.html', context)

@login_required
@staff_member_required
def admin_order_detail(request, order_id):
    """
    View function for displaying order details.
    """
    order = get_object_or_404(Order, id=order_id)
    return JsonResponse({
        'id': order.id,
        'shipping_name': order.shipping_name,
        'shipping_email': order.shipping_email,
        'shipping_phone': order.shipping_phone,
        'shipping_address': order.shipping_address,
        'total_amount': str(order.total_amount),
        'status': order.status,
        'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'items': [
            {
                'product_name': item.product_name,
                'product_price': str(item.product_price),
                'quantity': item.quantity,
                'subtotal': str(item.subtotal),
                'product_image': item.product_image,
            }
            for item in order.items.all()
        ]
    })

@login_required
@staff_member_required
def admin_chat_messages(request, feedback_id):
    """
    View function for loading chat messages for a specific feedback.
    """
    feedback = get_object_or_404(OrderFeedback, id=feedback_id)
    messages = feedback.messages.all().order_by('created_at')
    
    return JsonResponse({
        'messages': [
            {
                'id': message.id,
                'message_type': message.message_type,
                'message': message.message,
                'created_at': message.created_at.strftime('%H:%M'),
            }
            for message in messages
        ]
    })

@login_required
@staff_member_required
def admin_send_message(request, feedback_id):
    """
    View function for sending a message in a chat.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    feedback = get_object_or_404(OrderFeedback, id=feedback_id)
    message_text = request.POST.get('message', '').strip()
    
    if not message_text:
        return JsonResponse({'error': 'Message is required'}, status=400)
    
    message = ChatMessage.objects.create(
        feedback=feedback,
        order=feedback.order,
        message_type='agent',
        message=message_text
    )
    
    return JsonResponse({
        'id': message.id,
        'message_type': message.message_type,
        'message': message.message,
        'created_at': message.created_at.strftime('%H:%M'),
    })

@login_required
@staff_member_required
def admin_respond_feedback(request, feedback_id):
    """
    View function for responding to user feedback.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    feedback = get_object_or_404(OrderFeedback, id=feedback_id)
    response = request.POST.get('response', '').strip()
    
    if not response:
        return JsonResponse({'error': 'Response is required'}, status=400)
    
    feedback.admin_response = response
    feedback.save()
    
    return JsonResponse({
        'id': feedback.id,
        'admin_response': feedback.admin_response,
        'updated_at': feedback.updated_at.strftime('%Y-%m-%d %H:%M'),
    })

@login_required
@staff_member_required
def admin_mark_resolved(request, feedback_id):
    """
    View function for marking a feedback as resolved.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    feedback = get_object_or_404(OrderFeedback, id=feedback_id)
    feedback.is_resolved = True
    feedback.save()
    
    return JsonResponse({
        'id': feedback.id,
        'is_resolved': feedback.is_resolved,
    })

@login_required
@staff_member_required
def admin_update_order_status(request, order_id):
    """
    View function for updating order status.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    order = get_object_or_404(Order, id=order_id)
    status = request.POST.get('status')
    
    if status not in ['pending', 'processing', 'completed']:
        return JsonResponse({'error': 'Invalid status'}, status=400)
    
    order.status = status
    order.save()
    
    return JsonResponse({
        'id': order.id,
        'status': order.status,
    })