from http import HTTPStatus

import pytest
from django.urls import reverse

from product.constants import (
    CATEGORY_PAGINATOR_SIZE,
    PRODUCT_PAGINATOR_SIZE,
)


@pytest.mark.django_db
def test_categories_data(api_client, categories):
    """Проверит, доступ к списку категорий."""
    response = api_client.get(reverse('category-list'))
    data = response.data
    assert response.status_code == HTTPStatus.OK
    assert 'count' in data
    assert 'next' in data
    assert data['next'].endswith('?page=2')
    assert 'previous' in data
    assert 'results' in data
    assert len(data['results']) == CATEGORY_PAGINATOR_SIZE
    assert 'id' in data['results'][0]
    assert 'name' in data['results'][0]
    assert 'slug' in data['results'][0]
    assert 'image' in data['results'][0]


@pytest.mark.django_db
def test_category_data(api_client, category):
    """Проверит, доступ к конкретной категории."""
    response = api_client.get(
        reverse('category-detail', kwargs={'slug': 'slug-category'})
    )
    data = response.data
    assert response.status_code == HTTPStatus.OK
    assert 'id' in data
    assert 'name' in data
    assert 'slug' in data
    assert 'image' in data
    assert data['name'] == 'name-category'
    assert data['slug'] == 'slug-category'
    assert data['image'].endswith('image-category')


@pytest.mark.django_db
def test_products_data(api_client, products):
    """Проверит, доступ к списку продуктов."""
    response = api_client.get(reverse('product-list'))
    data = response.data
    assert response.status_code == HTTPStatus.OK
    assert 'count' in data
    assert 'next' in data
    assert data['next'].endswith('?page=2')
    assert 'previous' in data
    assert 'results' in data
    assert len(data['results']) == PRODUCT_PAGINATOR_SIZE
    assert 'id' in data['results'][0]
    assert 'name' in data['results'][0]
    assert 'slug' in data['results'][0]
    assert 'price' in data['results'][0]
    assert 'image' in data['results'][0]
    assert 'image_thumbnail' in data['results'][0]
    assert 'image_medium' in data['results'][0]


@pytest.mark.django_db
def test_product_data(api_client, product):
    """Проверит, доступ к конкретному продукту."""
    response = api_client.get(
        reverse('product-detail', kwargs={'slug': 'slug-product'})
    )
    data = response.data
    assert response.status_code == HTTPStatus.OK
    assert 'id' in data
    assert 'name' in data
    assert 'slug' in data
    assert 'price' in data
    assert 'image' in data
    assert 'image_thumbnail' in data
    assert 'image_medium' in data
    assert data['name'] == 'name-product'
    assert data['slug'] == 'slug-product'
    assert data['price'] == '999.99'
