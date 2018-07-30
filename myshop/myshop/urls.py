"""myshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static


# This is project folder urls

urlpatterns = [
    path('admin/', admin.site.urls),

    # This needs to be added before shop urls
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^orders/', include('orders.urls', namespace='orders')),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^payment/', include('payment.urls', namespace='payment')),
    url(r'^coupons/', include('coupons.urls', namespace='coupons')),
    # to add urls for shop application
    # namespace to differentiate two same url name from two different apps, like shop/product , warehouse/product
    url(r'^', include('shop.urls', namespace='shop')),


]

# We only serve static files in development. Never serve static files in production
if settings.DEBUG:
    # urlpatterns+= [ url(r'^media/(?P<path>.*)',serve,{'document_root':settings.MEDIA_ROOT, }), ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
