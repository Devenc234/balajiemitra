from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart
        :param request:
        """

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

        # store current applied coupon
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update quantity of cart
        :param product: product which needs to be added
        :param quantity: by default 1
        :param update_quantity: be default False
        :return:
        """
        # We use product_id to remember what has been added to cart till now.
        # We have converted product_id to string because django uses json to serialize session data
        # and json allow only string string for keys. for value part, we can put integers but not decimal
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart
        :param product: product object which need to removed
        :return:
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the product_id in the cart and get the product form the backend
        :return:
        """
        product_ids = self.cart.keys()

        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price']*item['quantity']
            yield item

    def __len__(self):
        """
        count all the items in the cart
        :return:
        """
        return sum(item['quantity'] for item in self.cart.values())

    # TODO: Need to change UI for get_total_price or get_total_price_after_discount after adding discount
    # currently for cart detail and invoice, after applying discount, old total cost printed
    def get_total_price(self):
        # Because we are not using iter method here, so price comes as string. we have to convert price to decimal
        return sum(item['quantity']*Decimal(item['price']) for item in self.cart.values())

    def clear(self):
        """
        To empty the cart
        :return:
        """
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal('100')) \
                   * self.get_total_price()
        return Decimal('0')

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
