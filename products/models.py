import os
import random

from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.urls import reverse

from eCommerce_Django.utils import unique_slug_generator, get_filename


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 4000000000)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return 'products/{new_filename}/{final_filename}'.format(new_filename=new_filename,final_filename=final_filename)


class Category(models.Model):
    name = models.CharField(max_length=30)
    ordering = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['ordering']


class ProductQuerySet(models.query.QuerySet):
    in_cart = models.BooleanField(default=False)

    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

    def search(self, query):
        lookups = (Q(title__icontains=query) | Q(description__icontains=query) | Q(price__icontains=query) | Q(tag__title__icontains=query))
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)


class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    grammage = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    delivery = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    objects = ProductManager()

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    @property
    def name(self):
        return self.title


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)


def upload_product_file_loc(instance, filename):
    slug = instance.product.slug
    id_ = instance.id
    if id_ is None:
        Klass = instance.__class__
        qs = Klass.objects.all().order_by('-pk')
        if qs.exists():
            id_ = qs.first().id + 1
        else:
            id_ = 0
    if not slug:
        slug = unique_slug_generator(instance.product)
    location = "product/{slug}/{id}".format(slug=slug, id=id_)
    return location + filename


class ProductFile(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, default='', null=True, blank=True)
    description = models.TextField(default='', null=True, blank=True)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)

    @property
    def display_name(self):
        if self.name:
            return self.name
        og_name = get_filename(self.image.name)
        return og_name

    def get_default_url(self):
        return self.product.get_absolute_url()
