from django.db import models
from product.models import Product
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed


STATUS = [
    # letf side: DB
    # right side: human-readable name
    ('waiting','Bekleniyor'),
    ('buyed','Satinalindi'),
    ('deleted','Silindi'),
]
#Cart
#CartItem - > Product

class ShoppingCartItem(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        )
    price = models.FloatField(default=0)
    is_deleted = models.BooleanField(default=False)
    createt_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.title} price: {self.price} TL"


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, 
        blank=True, 
        null=True,
        on_delete=models.CASCADE)
    session_key = models.CharField(max_length = 32, blank=True, null= True)
    items = models.ManyToManyField(ShoppingCartItem, blank=True)
    total_price = models.FloatField(default=0)
    status = models.CharField(
        default = 'waiting',
        choices = STATUS,
        max_length = 10,
    )
    createt_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"PK: {self.pk} - Total: {self.total_price} - Status: {self.status}"
    
    def total_price_update(self):
        if self.status == 'waiting':
            total_price = 0
            for item in self.items.all():
                if item.is_deleted == False:
                    total_price += item.price
            self.total_price = total_price
            self.save()


@receiver(post_save, sender=ShoppingCartItem)
def shopping_card_item_receiver(sender, created, instance, *args, **kwargs):
    if created:
        instance.price = instance.product.price
        instance.save()
    instance.shoppingcart_set.first().total_price_update()


@receiver(m2m_changed, sender = ShoppingCart.items.through)
def shopping_card_receiver(sender, instance, *args, **kwargs):
    instance.total_price_update()
    