from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from .models import GroceryBasketUser


@register(GroceryBasketUser)
class UsersAdmin(UserAdmin):
    """Модель для зоны администрирования."""
