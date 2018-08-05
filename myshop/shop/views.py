from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.http import Http404
from cart.forms import CartAddProductForm
from shop.recommender import Recommender
# Create your views here.

# Here category slug is an optional parameter.
# We are creating only one view for products and products/<category>


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)  # only selecting available products
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'shop/products/list.html', context={'category': category,
                                                               'categories': categories,
                                                               'products': products},)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    return render(request, 'shop/products/detail.html', context={'product': product,
                                                                 'cart_product_form': cart_product_form,
                                                                 'recommended_products': recommended_products},)

