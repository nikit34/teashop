from django.contrib import admin

from .models import BundleItem, Category, Product, ProductFile


class ProductFileInline(admin.TabularInline):
    model = ProductFile
    extra = 1


class BundleItemInline(admin.TabularInline):
    model = BundleItem
    fk_name = 'bundle'
    extra = 1
    autocomplete_fields = ['item']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug', 'price', 'category', 'active']
    list_filter = ['category', 'active', 'featured']
    search_fields = ['title']
    inlines = [BundleItemInline, ProductFileInline]

    class Meta:
        model = Product

    class Media:
        js = ('/static/js/tinyInject.js',)


admin.site.register(Product, ProductAdmin)


admin.site.register(Category)
