from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    SerializerMethodField,
)

from .models import Cart, CartProduct


class CartProductSerializer(ModelSerializer):

    product = SerializerMethodField()
    price = SerializerMethodField()
    total_price = SerializerMethodField()

    class Meta:
        model = CartProduct
        fields = 'product', 'quantity', 'price', 'total_price'

    def get_product(self, obj):
        """Вернет название продукта в поле product."""
        return obj.product.name

    def get_price(self, obj):
        """Вернет цену в поле price."""
        return obj.product.price

    def get_total_price(self, obj):
        """Вернет общую цену продукта в поле total_price."""
        return obj.total_price


class CartResponseSerializer(ModelSerializer):

    products = CartProductSerializer(many=True, read_only=True)
    total_price = SerializerMethodField()

    class Meta:
        model = Cart
        fields = 'id', 'user', 'total_price', 'products'

    def get_total_price(self, obj):
        """Вернет общую цену продуктов корзины в поле total_price."""
        return obj.total_price


class CreateUpdateCartProductSerializer(ModelSerializer):

    class Meta:
        model = CartProduct
        fields = 'product', 'quantity'


class BulkCreateUpdateCartProductSerializer(Serializer):
    """Сериализатор для добавления, обновления и удаления продуктов из корзины.

    Подразумевается, что:
    - добавлять новые продукты можно только POST-запросом;
    - PUT и PATCH запросы изменяют только количество продукта в корзине,
      и только того, что есть в корзине - остальное игнорируется;
    - DELETE запрос полностью очищает корзину.
    """

    products = CreateUpdateCartProductSerializer(many=True)

    def create(self, validated_data):
        """Обрабатывает логику создания записи в корзине.

        Автоматически определит корзину пользователя.
        Если продукта не было в корзине - добавит его.
        Если продукт был в корзине, удалит его и добавит с новым количеством.
        """
        cart = self.context['request'].user.cart
        items_data = validated_data.pop('products')
        check_list = [item['product'] for item in items_data]

        CartProduct.objects.filter(
            cart=cart,
            product__in=check_list,
        ).delete()

        items = [
            CartProduct(cart=cart, **item_data)
            for item_data in items_data
        ]
        CartProduct.objects.bulk_create(items)
        return cart

    def update(self, validated_data):
        """Обрабатывает логику обновления количества продуктов в корзине.

        Автоматически определит корзину пользователя.
        Если продукта не было в корзине - добавит его.
        Если продукт был в корзине, удалит его и добавит с новым количеством.
        """
        cart = self.context['request'].user.cart

        items_data = validated_data.pop('products')
        updates = {item['product_id']: item['quantity'] for item in items_data}

        items_to_update = CartProduct.objects.filter(
            cart=cart,
            product_id__in=updates.keys()
        )
        for item in items_to_update:
            item.quantity = updates[item.product]

        return cart

    def to_representation(self, instance):
        """
        Переопределяет данные в нужный формат для ответа.
        """
        return CartResponseSerializer(instance=instance).data
