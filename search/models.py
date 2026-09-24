from django.db import models

from products.models import Product


class ProductEmbedding(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="embedding")
    vector = models.JSONField(default=list)
    model_name = models.CharField(max_length=120)
    dim = models.PositiveIntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Embedding<{product}>".format(product=self.product_id)
