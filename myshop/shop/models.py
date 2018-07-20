from django.db import models
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    # How category object name will be displayed in Admin site
    def __str__(self):
        return self.name

    # To retrieve a url for a given object
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=True)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)  # will need to install pillow for this
    description = models.CharField(max_length=1000, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # decimal, avoid error due to rounding off
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)  # To remove product,if not available
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        index_together = [['id', 'slug'], ]  # To query product based on ID and slug both

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # args=[self.id, self.slug] ---> this will add id and slug . eg 8/mylaptop
        # forward comes automatically and because of that I wasted 5 hours debugging it.
        # id is self generated for Product model.
        return reverse('shop:product_detail', args=[self.id, self.slug])
