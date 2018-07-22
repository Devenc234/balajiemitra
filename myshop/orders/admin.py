from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]


# admin.site.register(Order, OrderAdmin)
# Please keep note on above thing. We are registering Order model with OrderAdmin, not OrderItem nor OrderItemInline
# To avoid this, we can use annotation as I have used above

# Also OrderItemInline has to written above OrderAdmin class
