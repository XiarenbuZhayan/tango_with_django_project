from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def index(request):
    return HttpResponse("Welcome")

def homepage(request):
    return render(request, "homepage.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        
        # 检查是否已经提交了密码
        password = request.POST.get('password')
        
        if password:  # 如果提交了密码，进行完整的登录流程
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