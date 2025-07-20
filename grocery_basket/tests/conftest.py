from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from product.models import Category, Product, Subcategory

User = get_user_model()

NUMBER_CATEGORIES = 50
RATIO_SUBCATEGORIES = 4


@pytest.fixture
def api_client():
    """Фикстура для неавторизованного клиента API."""
    return APIClient()


@pytest.fixture
def authenticated_api_client(api_client):
    """Фикстура для авторизованного клиента API."""
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    api_client.force_authenticate(user=user)
    return api_client, user


@pytest.fixture
def two_authenticated_api_clients():
    """Фикстура для двух авторизованных клиента API."""
    first_user = User.objects.create(
        username='first',
        email='first@example.com',
        password='testpass123',
    )
    second_user = User.objects.create(
        username='second',
        email='second@example.com',
        password='testpass123'
    )
    first_api_client = APIClient()
    second_api_client = APIClient()
    first_api_client.force_authenticate(user=first_user)
    second_api_client.force_authenticate(user=second_user)
    return first_api_client, first_user, second_api_client, second_user


@pytest.fixture
def subcategories(categories):
    """Фикстура создаст и вернет категории и подкатегории."""
    subcategories = Subcategory.objects.bulk_create([
        Subcategory(
            slug=str(i),
            name=str(i),
            image=str(i),
            category=categories[i // RATIO_SUBCATEGORIES],
        )
        for i in range(NUMBER_CATEGORIES * RATIO_SUBCATEGORIES)
    ])
    return categories, subcategories


@pytest.fixture
def categories():
    """Фикстура создаст и вернет категории."""
    return Category.objects.bulk_create([
        Category(slug=str(i), name=str(i), image=str(i))
        for i in range(NUMBER_CATEGORIES)
    ])


@pytest.fixture
def category():
    """Фикстура создаст и вернет категорию."""
    return Category.objects.create(
        slug='slug-category',
        name='name-category',
        image='image-category',
    )


@pytest.fixture
def products(subcategories):
    """Фикстура создаст продукты."""
    categories, subcategories = subcategories
    return Product.objects.bulk_create([
        Product(
            slug=str(i),
            name=str(i),
            price=i + 1,
            category=categories[i],
            subcategory=subcategories[i * RATIO_SUBCATEGORIES],
        )
        for i in range(NUMBER_CATEGORIES)
    ])


@pytest.fixture
def subcategory(category):
    """Фикстура создаст и вернет категорию и подкатегорию."""
    subcategory = Subcategory.objects.create(
            slug='slug-subcategory',
            name='name-subcategory',
            image='image-subcategory',
            category=category,
        )
    return category, subcategory


@pytest.fixture
def product(subcategory):
    """Фикстура создаст и вернет конкретный продукт."""
    category, subcategory = subcategory
    products = Product.objects.bulk_create([
        Product(
            slug='slug-product',
            name='name-product',
            price=Decimal('999.99'),
            category=category,
            subcategory=subcategory,
        )
    ])
    return products[0]
