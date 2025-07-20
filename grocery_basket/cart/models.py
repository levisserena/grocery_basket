from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.mixins import DateAutoMixin
from product.models import Product

User = get_user_model()


class Cart(DateAutoMixin):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Хозяин корзины',
    )

    def __repr__(self):
        return f'Cart(user_id={self.user.id})'

    @property
    def total_price(self):
        """Свойство для подсчета общей стоимости всех продуктов в корзине."""
        return sum(product.total_price for product in self.products.all())


class CartProduct(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт',
    )
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Корзина',
    )
    quantity = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1, message='Значение не может быть меньше 1'),
        ],
        verbose_name='Количество',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['cart', 'product'],
                name='unique_cart_product',
            )
        ]

    @property
    def total_price(self):
        """
        Свойство для подсчета общей стоимости определенного продукта в корзине.
        """
        return self.product.price * self.quantity


@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    """При создании пользователя создаст для него корзину."""
    if created:
        Cart.objects.create(user=instance)
