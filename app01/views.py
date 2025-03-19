from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
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

def logout(request):
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
    return render(request, 'bag.html')

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

def notebook(request):
    """
    View function for displaying notebook page
    """
    return render(request, 'notebook.html')

def earphone(request):
    """
    View function for displaying earphone page
    """
    return render(request, 'earphone.html')

def accessory(request):
    """
    View function for displaying accessory page
    """
    return render(request, 'accessory.html')

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
                        {'size': '1T', 'price': 1499}
                    ]
                },
                {
                    'name': 'iPhone 16 Pro Max',
                    'display_size': '6.7-inch display',
                    'price': 1199,
                    'storage_options': [
                        {'size': 256, 'price': 1199},
                        {'size': 512, 'price': 1399},
                        {'size': '1T', 'price': 1599}
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
                {'size': '1T', 'price': 1499}
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