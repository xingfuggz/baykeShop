from django.contrib import admin
from django.template.loader import render_to_string

# Register your models here.
from baykeshop.site.admin import site as bayke_site
from .models import *


@admin.register(BaykeShopOrder, site=bayke_site)
class BaykeShopOrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_sn', 'user', 'order_skus', 
        'pay_price', 'status', 'pay_type', 
        'is_verify', 'pay_time', 'create_time'
    )
    list_filter = ('pay_type', 'status',)
    search_fields = ('order_sn', 'user__username',)
    readonly_fields = (
        'user', 'order_sn', 'pay_id', 
        'total_price', 'pay_time', 'pay_type', 
        # 'status', 
        'is_verify', 'order_skus'
    )
    exclude = ('is_delete',)
    actions = ['shipments', 'verify']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('baykeshoporderitem_set')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        # 未支付和未发货订单可操作修改
        # if obj and obj.status not in [0, 1]:
        #     return False
        return super().has_change_permission(request, obj)
    
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        # 已支付订单不能再修改支付金额
        if obj and obj.status == BaykeShopOrder.OrderStatus.WAIT_DELIVER:
            readonly_fields = list(readonly_fields) + ['pay_price'] 
        return readonly_fields
    
    @admin.display(description='订单商品')
    def order_skus(self, obj):
        queryset = obj.baykeshoporderitem_set.all()
        return render_to_string('order/orderitems.html', {'queryset': queryset})
    
    @admin.action(description='所选订单 发货')
    def shipments(self, request, queryset):
        for item in queryset:
            if item.status != BaykeShopOrder.OrderStatus.WAIT_DELIVER: 
                continue
            BaykeShopOrderLog.create_log(item, '订单已发货', request.user)
            item.status = BaykeShopOrder.OrderStatus.WAIT_RECEIVE
            item.save()
        self.message_user(request, '操作成功')
    
    @admin.action(description='所选订单 核销')
    def verify(self, request, queryset):
        for item in queryset:
            if item.status != BaykeShopOrder.OrderStatus.WAIT_VERIFY: 
                continue
            item.status = BaykeShopOrder.OrderStatus.WAIT_EVALUATE
            item.is_verify = True
            item.pay_time = timezone.now()
            item.save()
            BaykeShopOrderLog.create_log(item, '订单已核销', request.user)
        self.message_user(request, '操作成功')


@admin.register(BaykeShopOrderLog, site=bayke_site)
class BaykeShopOrderLogAdmin(admin.ModelAdmin):
    list_display = ('content', 'order', 'type', 'user', 'create_time')
    list_filter = ('type',)
    search_fields = ('content', 'order__order_sn',)
    readonly_fields = ('order', 'type', 'content', 'user', 'create_time')
    exclude = ('user',)

    def has_add_permission(self,request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False