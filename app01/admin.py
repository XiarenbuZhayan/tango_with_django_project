from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.html import format_html
from .models import Order, OrderItem, OrderFeedback, UserPaymentInfo

# 注释掉OrderFeedback的导入
# from .models import Order, OrderItem, OrderFeedback, UserPaymentInfo

# 注释掉修改OrderFeedback在admin中的注册名称
# OrderFeedback._meta.verbose_name = 'Order Feedback Custom'
# OrderFeedback._meta.verbose_name_plural = 'Order Feedback Custom'

# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'shipping_name', 'shipping_email', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('shipping_name', 'shipping_email', 'shipping_phone')
    inlines = [OrderItemInline]

class OrderFeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_link', 'feedback_type_colored', 'subject', 'is_resolved_colored', 'created_at', 'action_buttons')
    list_filter = ('feedback_type', 'is_resolved', 'created_at')
    search_fields = ('subject', 'message', 'order__shipping_name')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:feedback_id>/reply/', self.admin_site.admin_view(self.feedback_reply_view), name='feedback_reply'),
        ]
        return custom_urls + urls
    
    def feedback_reply_view(self, request, feedback_id):
        feedback = OrderFeedback.objects.get(id=feedback_id)
        if request.method == 'POST':
            response = request.POST.get('response')
            feedback.admin_response = response
            feedback.is_resolved = True
            feedback.save()
            return JsonResponse({'status': 'success'})
            
        return render(request, 'admin/feedback_reply.html', {'feedback': feedback})
    
    def order_link(self, obj):
        """Create a link to the order detail page"""
        url = f"/admin/app01/order/{obj.order.id}/change/"
        return format_html('<a href="{}">{}</a>', url, f"Order #{obj.order.id}")
    order_link.short_description = 'Related Order'
    
    def feedback_type_colored(self, obj):
        """Display different colors for different feedback types"""
        colors = {
            'question': '#17a2b8',  # Blue
            'problem': '#dc3545',   # Red
            'suggestion': '#28a745' # Green
        }
        
        type_display = obj.get_feedback_type_display()
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.feedback_type, 'black'),
            type_display
        )
    feedback_type_colored.short_description = 'Feedback Type'
    
    def is_resolved_colored(self, obj):
        """Add color indicator for resolution status"""
        if obj.is_resolved:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">Resolved</span>'
            )
        else:
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;">Pending</span>'
            )
    is_resolved_colored.short_description = 'Status'
    
    def action_buttons(self, obj):
        """Add action buttons"""
        reply_url = f"/admin/app01/orderfeedback/{obj.id}/reply/"
        
        if obj.is_resolved:
            return format_html(
                '<a class="button" href="{}">View Details</a>',
                reply_url
            )
        else:
            return format_html(
                '<a class="button" style="background-color: #28a745; color: white;" href="{}">Reply</a>',
                reply_url
            )
    action_buttons.short_description = 'Actions'

class UserPaymentInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'firstName', 'surname', 'email', 'created_at')
    search_fields = ('firstName', 'surname', 'email', 'phone')

# 注册顺序决定了在Admin界面中的显示顺序
admin.site.register(OrderFeedback, OrderFeedbackAdmin)  # 放在最前面
admin.site.register(Order, OrderAdmin)
admin.site.register(UserPaymentInfo, UserPaymentInfoAdmin)
