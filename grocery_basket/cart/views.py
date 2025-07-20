from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import Cart
from .serializers import (
    BulkCreateUpdateCartProductSerializer,
    CartResponseSerializer,
)


class CartViewSet(ViewSet):
    """Набор методов обработчиков для эндпоинтов Корзины."""

    permission_classes = (IsAuthenticated,)

    def get_serializer(self, *args, **kwargs):
        """
        Возвращает экземпляр сериализатора, который следует использовать для
        проверки и десериализации входных данных, а также для сериализации
        выходных данных.
        """
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_serializer_context(self):
        """
        Дополнительный контекст, предоставляемый классу serializer.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer_class(self):
        """В зависимости от метода запроса вернет нужный сериализатор."""
        if self.action in ('create', 'update', 'partial_update'):
            return BulkCreateUpdateCartProductSerializer
        return CartResponseSerializer

    def _serializer_save(self, request):
        """
        Запустит валидацию сериализатора и сохранит результат.
        Вернет сериализованные данные.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def get(self, request, *args, **kwargs):
        """Переопределяет метод.

        Метод GET на эндпоинт вернет одну запись:
        корзину пользователя сделавшего запрос.
        """
        queryset = Cart.objects.get(user=request.user)
        serializer = self.get_serializer(queryset, many=False)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Обрабатывает POST запросы на /api/cart/"""
        return Response(
            self._serializer_save(request),
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        """Обрабатывает PUT запросы на /api/cart/"""
        return Response(
            self._serializer_save(request),
            status=status.HTTP_200_OK,
        )

    def partial_update(self, request, *args, **kwargs):
        """Обрабатывает PATCH запросы на /api/cart/"""
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Обрабатывает DELETE запросы на /api/cart/"""
        cart = Cart.objects.get(user=request.user)
        cart.delete()
        Cart.objects.create(user=request.user)
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
