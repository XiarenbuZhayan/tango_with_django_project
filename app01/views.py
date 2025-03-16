from django.shortcuts import render, redirect
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
    """
    View function for displaying phone detail page with configuration options
    """
    # Phone data dictionary - in a real app this would come from a database
    phones = {
        'iphone16pro': {
            'id': 'iphone16pro',
            'name': 'iPhone 16 Pro',
            'base_price': 999,
            'monthly_price': 41.62,
            'display_size': '6.3',
            'has_max_model': True,
            'max_price': 1199,
            'max_monthly_price': 49.95,
            'max_display_size': '6.9',
            'image_path': 'images/iphone_16pro__erw9alves2qa_xlarge_2x.png',
            'colors': [
                {'name': 'Natural Titanium', 'hex_code': '#e3ccb4', 'image_path': 'images/iphone_16pro__erw9alves2qa_xlarge_2x.png'},
                {'name': 'White Titanium', 'hex_code': '#f0e8d6', 'image_path': 'images/iphone_16pro__erw9alves2qa_xlarge_2x.png'},
                {'name': 'Silver Titanium', 'hex_code': '#f5f5f7', 'image_path': 'images/iphone_16pro__erw9alves2qa_xlarge_2x.png'},
                {'name': 'Black Titanium', 'hex_code': '#232324', 'image_path': 'images/iphone_16pro__erw9alves2qa_xlarge_2x.png'}
            ],
            'storage_options': [
                {'size': 128, 'price_add': 0, 'description': 'Good for most users with light storage needs'},
                {'size': 256, 'price_add': 100, 'description': 'Better for users who take lots of photos and videos'},
                {'size': 512, 'price_add': 300, 'description': 'Best for power users with large media libraries'},
                {'size': 1024, 'price_add': 500, 'description': 'Ideal for professionals working with large files'}
            ]
        },
        'iphone16': {
            'id': 'iphone16',
            'name': 'iPhone 16',
            'base_price': 799,
            'monthly_price': 33.29,
            'display_size': '6.1',
            'has_max_model': True,
            'max_price': 899,
            'max_monthly_price': 37.45,
            'max_display_size': '6.7',
            'image_path': 'images/iphone_16__c5bvots96jee_xlarge_2x.png',
            'colors': [
                {'name': 'Blue', 'hex_code': '#7c98c6', 'image_path': 'images/iphone_16__c5bvots96jee_xlarge_2x.png'},
                {'name': 'White', 'hex_code': '#f5f5f7', 'image_path': 'images/iphone_16__c5bvots96jee_xlarge_2x.png'},
                {'name': 'Pink', 'hex_code': '#ffd2e5', 'image_path': 'images/iphone_16__c5bvots96jee_xlarge_2x.png'},
                {'name': 'Black', 'hex_code': '#232324', 'image_path': 'images/iphone_16__c5bvots96jee_xlarge_2x.png'}
            ],
            'storage_options': [
                {'size': 128, 'price_add': 0, 'description': 'Good for most users with light storage needs'},
                {'size': 256, 'price_add': 100, 'description': 'Better for users who take lots of photos and videos'},
                {'size': 512, 'price_add': 300, 'description': 'Best for power users with large media libraries'}
            ]
        },
        'iphone16e': {
            'id': 'iphone16e',
            'name': 'iPhone 16e',
            'base_price': 599,
            'monthly_price': 24.95,
            'display_size': '6.1',
            'has_max_model': False,
            'image_path': 'images/iphone_16e__cubm3xoy5qaa_xlarge_2x.png',
            'colors': [
                {'name': 'Black', 'hex_code': '#232324', 'image_path': 'images/iphone_16e__cubm3xoy5qaa_xlarge_2x.png'}
            ],
            'storage_options': [
                {'size': 128, 'price_add': 0, 'description': 'Good for most users with light storage needs'},
                {'size': 256, 'price_add': 100, 'description': 'Better for users who take lots of photos and videos'}
            ]
        },
        'iphone15': {
            'id': 'iphone15',
            'name': 'iPhone 15',
            'base_price': 699,
            'monthly_price': 29.12,
            'display_size': '6.1',
            'has_max_model': True,
            'max_price': 799,
            'max_monthly_price': 33.29,
            'max_display_size': '6.7',
            'image_path': 'images/iphone_15__buwagff0mwwi_xlarge_2x.png',
            'colors': [
                {'name': 'Yellow', 'hex_code': '#ffe7b9', 'image_path': 'images/iphone_15__buwagff0mwwi_xlarge_2x.png'},
                {'name': 'Green', 'hex_code': '#c1e1c5', 'image_path': 'images/iphone_15__buwagff0mwwi_xlarge_2x.png'},
                {'name': 'Blue', 'hex_code': '#b8c4d9', 'image_path': 'images/iphone_15__buwagff0mwwi_xlarge_2x.png'},
                {'name': 'Pink', 'hex_code': '#ffd2e5', 'image_path': 'images/iphone_15__buwagff0mwwi_xlarge_2x.png'},
                {'name': 'Black', 'hex_code': '#232324', 'image_path': 'images/iphone_15__buwagff0mwwi_xlarge_2x.png'}
            ],
            'storage_options': [
                {'size': 128, 'price_add': 0, 'description': 'Good for most users with light storage needs'},
                {'size': 256, 'price_add': 100, 'description': 'Better for users who take lots of photos and videos'},
                {'size': 512, 'price_add': 300, 'description': 'Best for power users with large media libraries'}
            ]
        }
    }
    
    # Get the phone data or return 404 if not found
    phone = phones.get(phone_id)
    if not phone:
        return HttpResponseNotFound("Phone not found")
    
    context = {
        'phone': phone
    }
    
    return render(request, 'phone_detail.html', context)

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