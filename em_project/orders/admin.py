from django.contrib import admin

from em_project.orders.models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_number', 'status',
                    'total_price', 'time_create', 'time_update')
    list_filter = ('status', 'time_create')
    search_fields = ('id', 'table_number')
    ordering = ('-time_create',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'dish_name', 'price')
    list_filter = ('order',)
    search_fields = ('dish_name',)
