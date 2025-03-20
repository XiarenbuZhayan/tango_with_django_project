from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
import re
import json

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
    if not request.user.is_authenticated:
        return redirect('signin')
    return render(request, 'my_orders.html')

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