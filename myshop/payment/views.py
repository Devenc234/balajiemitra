from decimal import Decimal
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render,get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from orders.models import Order


@csrf_exempt
def payment_done(request):
    return render(request, 'payment/done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')


# view_that_asks_for_money
def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()

    paypal_dict = {
        "business": "devendra072@gmail.com",
        "amount": '%.2f' % order.get_total_cost().quantize(Decimal('0.01')),
        "item_name": 'Order {}'.format(order.id),
        "invoice": str(order.id),
        "currency_code": 'USD',
        # "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        # "return": request.build_absolute_uri(reverse('your-return-view')),
        # "cancel_return": request.build_absolute_uri(reverse('your-cancel-view')),
        "notify_url": 'http://{}{}'.format(host, reverse('paypal-ipn')),
        "return": 'http://{}{}'.format(host, reverse('payment:done')),
        "cancel_return": 'http://{}{}'.format(host, reverse('payment:canceled')),
        # "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"order": order,
               "form": form}
    return render(request, "payment/process.html", context)
