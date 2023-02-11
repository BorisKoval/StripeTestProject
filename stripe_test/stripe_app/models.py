import stripe
from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_id = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.product_id:
            product = stripe.Product.create(
                name=self.name,
                type='service',
            )
            self.product_id = product.id

        super().save(*args, **kwargs)
