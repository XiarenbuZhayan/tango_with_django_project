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
    path('signout/', views.signout, name='signout'),
    path('ipad/', views.ipad, name='ipad'),
    path('ipadmini/', views.ipadmini, name='ipadmini'),
    path('ipadpro/', views.ipadpro, name='ipadpro'),
    path('ipadair/', views.ipadair, name='ipadair'),
    path('laptop/', views.laptop, name='laptop'),
    path('macbookpro16/', views.macbookpro16, name='macbookpro16'),
    path('macbookpro14/', views.macbookpro14, name='macbookpro14'),
    path('macbookair13/', views.macbookair13, name='macbookair13'),
    path('macbookair15/', views.macbookair15, name='macbookair15'),
    path('phone/', views.phone, name='phone'),
    path('iphone16pro/', views.iphone16pro, name='iphone16pro'),
    path('iphone16/', views.iphone16, name='iphone16'),
    path('personal-info/', views.personal_info, name='personal_info'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('bag/', views.bag, name='bag'),
    path('add-to-bag/', views.add_to_bag, name='add_to_bag'),
    path('remove-from-bag/', views.remove_from_bag, name='remove_from_bag'),
    path('phone/<int:phone_id>/', views.phone_detail, name='phone_detail'),
    path('tablet/', views.tablet, name='tablet'),
    path('watch/', views.watch, name='watch'),
    path('watch-se/', views.watch_se, name='watch_se'),
    path('watch-series-10/', views.watch_series_10, name='watch_series_10'),
    path('watch-ultra-2/', views.watch_ultra_2, name='watch_ultra_2'),
    path('accessory/', views.accessory, name='accessory'),
    path('airtag/', views.airtag, name='airtag'),
    path('magsafe-charger/', views.magsafe_charger, name='magsafe_charger'),
    path('apple-pencil/', views.apple_pencil, name='apple_pencil'),
    path('iphone-cases/', views.iphone_cases, name='iphone_cases'),
    path('magic-mouse/', views.magic_mouse, name='magic_mouse'),
    path('magic-keyboard/', views.magic_keyboard, name='magic_keyboard'),
    path('homepod-mini/', views.homepod_mini, name='homepod_mini'),
    path('airpods-pro/', views.airpods_pro, name='airpods_pro'),
]
