import datetime
from django.contrib import admin
from django.http import HttpResponse
from .models import Order, OrderItem
from csv import writer
from django.utils.html import format_html
from django.urls import reverse

# Register your models here.


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts.verbose_name)
    csv_writer = writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # write the header row
    csv_writer.writerow([field.verbose_name for field in fields])
    # write data row
    for obj in queryset:
        datarow = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%y')
            datarow.append(value)
        csv_writer.writerow(datarow)
    return response


export_to_csv.short_description = 'Export to CSV'


# This needs to above OrderItemInline class
def order_detail(obj):
    # return '<a href="{}">View</a>'.format(
    #     reverse('orders:admin_order_detail', args=[obj.id]))
    return format_html('<a href="{}">View</a>'.format(
            reverse('orders:admin_order_detail', args=[obj.id])))


order_detail.allow_tags = True


# This class needs to above OrderAdmin class
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', order_detail]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]


# admin.site.register(Order, OrderAdmin)
# Please keep note on above thing. We are registering Order model with OrderAdmin, not OrderItem nor OrderItemInline
# To avoid this, we can use annotation as I have used above

# Also OrderItemInline has to written above OrderAdmin class
