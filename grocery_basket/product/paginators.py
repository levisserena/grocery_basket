from rest_framework.pagination import PageNumberPagination

from .constants import CATEGORY_PAGINATOR_SIZE, PRODUCT_PAGINATOR_SIZE


class CategoryPagination(PageNumberPagination):
    """Пагинатор для категорий."""

    page_size = CATEGORY_PAGINATOR_SIZE


class ProductPagination(PageNumberPagination):
    """Пагинатор для продуктов."""

    page_size = PRODUCT_PAGINATOR_SIZE
