from django.db import models
from shop.models import Product

# Template Database Design for Order,OrderItems
# http://techstream.org/Bits/Model-Design-for-Orders-in-Django


# Create your models here.
class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=150)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    paid = models.BooleanField(default=False)
    # auto_now_add : It is set only on create. If you use auto_now_add then you cannot set the field on your model
    #                manually. When you save, it will be set to the current date, regardless of any value you’ve set
    # auto_now     : It will update every time you save the model. Think of it like a "last modified" field
    # https://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    # when using foreign key relationship, on delete what should be done?
    # https://stackoverflow.com/questions/38388423/what-does-on-delete-do-on-django-models
    order = models.ForeignKey(Order, models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, models.PROTECT, related_name='order_items')

    # TODO : How to change price field to take value based on the Product.price
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.quantity*self.price
