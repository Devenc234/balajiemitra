# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery.task import task
from .models import Order
from django.core.mail import send_mail

# It is recommended to keep only id as input for task function. We can look up for order from ID.

# celery = Celery('myshop', broker='amqp://guest@localhost//')

@task
def order_created(order_id):
    """
    Task to send an e-mail when order is successfully created
    :param order_id:
    :return:
    """
    order = Order.objects.get(id=order_id)
    subject = 'Order number: {}'.format(order_id)
    message = 'Dear {},' \
              '\n\nYou have successfully placed an order. Your order id is {}.'.format(order.first_name, order_id)
    mail_sent = send_mail(subject, message, 'devenc234@gmail.com', [order.email])
    return mail_sent
