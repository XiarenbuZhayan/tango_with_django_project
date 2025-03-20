from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bag/', views.bag, name='bag'),
    path('payment_check/', views.payment_check, name='payment_check'),
    path('checkout/', views.checkout, name='checkout'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('success/', views.success, name='success'),
    # 其他URL模式...
    
    # 移除聊天相关URL
    # path('api/order-chat/<int:order_id>/', views.get_order_chat_messages, name='get_order_chat_messages'),
    path('order-feedback/', views.order_feedback, name='order_feedback'),
    path('order-feedback-history/<int:order_id>/', views.order_feedback_history, name='order_feedback_history'),
    path('admin-feedback-list/', views.admin_feedback_list, name='admin_feedback_list'),
    path('admin-feedback-response/', views.admin_feedback_response, name='admin_feedback_response'),
    path('admin-feedback-resolve/', views.admin_feedback_resolve, name='admin_feedback_resolve'),
    
    # Admin panel URLs
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin-update-order/<int:order_id>/', views.admin_update_order_status, name='admin_update_order_status'),
    path('admin-chat/<int:feedback_id>/', views.admin_chat_messages, name='admin_chat_messages'),
    path('admin-send-message/<int:feedback_id>/', views.admin_send_message, name='admin_send_message'),
    path('admin-respond-feedback/<int:feedback_id>/', views.admin_respond_feedback, name='admin_respond_feedback'),
    path('admin-mark-resolved/<int:feedback_id>/', views.admin_mark_resolved, name='admin_mark_resolved'),
] 