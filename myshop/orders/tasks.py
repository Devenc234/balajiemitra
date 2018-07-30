# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery.task import task
from django.template.loader import render_to_string
import weasyprint
from .models import Order, OrderItem
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from io import BytesIO

# It is recommended to keep only id as input for task function. We can look up for order from ID.

# celery = Celery('myshop', broker='amqp://guest@localhost//')


@task
def order_created(order_id):
    """
    Task to send an e-mail when orders is successfully created
    :param order_id:
    :return:
    """
    order = Order.objects.get(id=order_id)
    # orderitems = OrderItem.get(id=order_id)
    # print(orderitems)
    # subject = 'Order number: {}'.format(order_id)
    # message = 'Dear {} {},' \
    #           '\n\nYou have successfully placed an order. The details are as following:' \
    #           '\n order id: {}' \
    #           '\n order total cost: {}' \
    #           '\n order paid status: {}' \
    #           '\n Delivery address: {}, {}, PostCode:{}' \
    #           '\n\n Thank you for shopping with Balaji-e-mitra services' \
    #           ''.format(order.first_name, order.last_name, order_id, order.get_total_cost(), order.paid,
    #                     order.address, order.city, order.postal_code)
    # print(message)
    # mail_sent = send_mail(subject, message, 'devenc234@gmail.com', [order.email])
    # return mail_sent

    # create invoice e - mail
    subject = 'Balaji-e-mitra Services - Invoice no. {}'.format(order.id)
    message = 'Dear {} {},' \
              '\n\nYou have successfully placed an order. The details are as following:' \
              '\n order id: {}' \
              '\n order total cost: {}' \
              '\n order paid status: {}' \
              '\n Delivery address: {}, {}, PostCode:{}' \
              '\n\n Thank you for shopping with Balaji-e-mitra services' \
              ''.format(order.first_name, order.last_name, order_id, order.get_total_cost(), order.paid, order.address,
                        order.city, order.postal_code)
    email = EmailMessage(subject,
                         message,
                         'devenc234@gmail.com',
                         [order.email])

    # generate PDF
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out,
                                           stylesheets=stylesheets)
    # attach PDF file
    email.attach('order_{}.pdf'.format(order.id),
                 out.getvalue(),
                 'application/pdf')
    # send e-mail
    mail_sent = email.send()

    return mail_sent
