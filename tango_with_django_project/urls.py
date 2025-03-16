"""tango_with_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('index/', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('personal-info/', views.personal_info, name='personal_info'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('bag/', views.bag, name='bag'),
    path('phone/', views.phone, name='phone'),
    path('phone/<str:phone_id>/', views.phone_detail, name='phone_detail'),
    path('tablet/', views.tablet, name='tablet'),
    path('notebook/', views.notebook, name='notebook'),
    path('earphone/', views.earphone, name='earphone'),
    path('accessory/', views.accessory, name='accessory'),
]
