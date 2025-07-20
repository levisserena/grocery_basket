from decimal import Decimal
from http import HTTPStatus

import pytest
from django.urls import reverse

from cart.models import Cart, CartProduct
from product.models import Product


@pytest.mark.django_db
def test_no_authentication_access(api_client):
    """Не аутентифицированный пользователь не получит доступ."""
    response_get = api_client.get(reverse('cart-actions'))
    response_post = api_client.post(reverse('cart-actions'))
    response_patch = api_client.patch(reverse('cart-actions'))
    response_put = api_client.put(reverse('cart-actions'))
    response_delete = api_client.delete(reverse('cart-actions'))
    assert response_get.status_code == HTTPStatus.UNAUTHORIZED
    assert response_post.status_code == HTTPStatus.UNAUTHORIZED
    assert response_patch.status_code == HTTPStatus.UNAUTHORIZED
    assert response_put.status_code == HTTPStatus.UNAUTHORIZED
    assert response_delete.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.django_db
def test_get_cart(two_authenticated_api_clients, product):
    """Проверка get запроса к корзине."""
    first_api_client, first_user, second_api_client, _ = (
        two_authenticated_api_clients
    )
    cart = Cart.objects.get(user=first_user)
    CartProduct.objects.create(
        product=product,
        cart=cart,
        quantity=60
    )
    response = first_api_client.get(reverse('cart-actions'))
    response_second_user = second_api_client.get(reverse('cart-actions'))
    assert response.status_code == HTTPStatus.OK
    assert 'id' in response.data
    assert 'user' in response.data
    assert 'total_price' in response.data
    assert 'products' in response.data
    assert response.data['total_price'] == Decimal('59999.40')
    assert len(response.data['products']) == 1
    assert len(response_second_user.data['products']) == 0, (
        'У второго пользователя не должно быть в корзине ничего'
    )
    assert 'product' in (data := response.data['products'][0])
    assert 'quantity' in data
    assert 'price' in data
    assert 'total_price' in data
    assert data['product'] == 'name-product'
    assert data['quantity'] == 60
    assert data['price'] == Decimal('999.99')
    assert data['total_price'] == Decimal('59999.40')


@pytest.mark.django_db
def test_post_cart(two_authenticated_api_clients, products):
    """Проверка post запроса к корзине."""
    first_api_client, _, _, second_user = two_authenticated_api_clients

    response = first_api_client.post(
        reverse('cart-actions'),
        format='json',
        data={
            "products": [
                {
                    "product": 1,
                    "quantity": 15
                },
                {
                    "product": 3,
                    "quantity": 25
                }
            ]
        }
    )

    assert response.status_code == HTTPStatus.CREATED
    assert 'id' in response.data
    assert 'user' in response.data
    assert 'total_price' in response.data
    assert 'products' in response.data
    assert response.data['total_price'] == Decimal('90')
    assert len(response.data['products']) == 2
    assert not CartProduct.objects.filter(
        cart=Cart.objects.get(user=second_user)
    ), 'Корзина второго пользователя должна быть пуста.'
    assert 'product' in (data := response.data['products'][0])
    assert 'quantity' in data
    assert 'price' in data
    assert 'total_price' in data
    assert data['product'] == '0'
    assert data['quantity'] == 15
    assert data['price'] == Decimal('1')
    assert data['total_price'] == Decimal('15')


@pytest.mark.django_db
def test_patch_cart(authenticated_api_client, products, product):
    """Проверка patch запроса к корзине."""
    api_client, user = authenticated_api_client
    CartProduct.objects.bulk_create([
        CartProduct(
            cart=Cart.objects.get(user=user),
            product=product,
            quantity=i + 1,
        )
        for i, product in enumerate(products[:5])
    ])
    QUANTITY_BEFORE = 7
    CartProduct.objects.create(
            cart=Cart.objects.get(user=user),
            product=product,
            quantity=QUANTITY_BEFORE,
    )
    check_product = Product.objects.get(slug=product.slug)

    response_before = api_client.get(reverse('cart-actions'))
    check_total_price_cart = response_before.data['total_price']

    for val in response_before.data['products']:
        if val['product'] == 'name-product':
            check_total_price_product = val['total_price']

    QUANTITY = 15
    response = api_client.patch(
        reverse('cart-actions'),
        format='json',
        data={
            "products": [
                {
                    "product": check_product.id,
                    "quantity": QUANTITY,
                }
            ]
        }
    )

    for val in response.data['products']:
        if val['product'] == 'name-product':
            check_total_price_product_after = val['total_price']

    assert response.status_code == HTTPStatus.OK
    assert 'id' in response.data
    assert 'user' in response.data
    assert 'total_price' in response.data
    assert 'products' in response.data
    assert response.data['total_price'] - check_product.price * QUANTITY == (
        check_total_price_cart - check_product.price * QUANTITY_BEFORE
    ), 'При изменение не изменилась общая сумма корзины.'
    assert len(response.data['products']) == 6
    assert 'product' in (data := response.data['products'][0])
    assert 'quantity' in data
    assert 'price' in data
    assert 'total_price' in data
    assert data['product'] == '0'
    assert data['quantity'] == 1
    assert data['price'] == Decimal('1')
    assert data['total_price'] == Decimal('1')
    assert (
        check_total_price_product_after - check_product.price * QUANTITY
    ) == (
        check_total_price_product - check_product.price * QUANTITY_BEFORE
    ), 'При изменение не изменилась общая сумма продукта.'


@pytest.mark.django_db
def test_put_cart(authenticated_api_client, products, product):
    """Проверка put запроса к корзине."""
    api_client, user = authenticated_api_client
    CartProduct.objects.bulk_create([
        CartProduct(
            cart=Cart.objects.get(user=user),
            product=product,
            quantity=i + 1,
        )
        for i, product in enumerate(products[:5])
    ])
    QUANTITY_BEFORE = 7
    CartProduct.objects.create(
            cart=Cart.objects.get(user=user),
            product=product,
            quantity=QUANTITY_BEFORE,
    )
    check_product = Product.objects.get(slug=product.slug)

    response_before = api_client.get(reverse('cart-actions'))
    check_total_price_cart = response_before.data['total_price']

    for val in response_before.data['products']:
        if val['product'] == 'name-product':
            check_total_price_product = val['total_price']

    QUANTITY = 15
    response = api_client.put(
        reverse('cart-actions'),
        format='json',
        data={
            "products": [
                {
                    "product": check_product.id,
                    "quantity": QUANTITY,
                }
            ]
        }
    )

    for val in response.data['products']:
        if val['product'] == 'name-product':
            check_total_price_product_after = val['total_price']

    assert response.status_code == HTTPStatus.OK
    assert 'id' in response.data
    assert 'user' in response.data
    assert 'total_price' in response.data
    assert 'products' in response.data
    assert response.data['total_price'] - check_product.price * QUANTITY == (
        check_total_price_cart - check_product.price * QUANTITY_BEFORE
    ), 'При изменение не изменилась общая сумма корзины.'
    assert len(response.data['products']) == 6
    assert 'product' in (data := response.data['products'][0])
    assert 'quantity' in data
    assert 'price' in data
    assert 'total_price' in data
    assert data['product'] == '0'
    assert data['quantity'] == 1
    assert data['price'] == Decimal('1')
    assert data['total_price'] == Decimal('1')
    assert (
        check_total_price_product_after - check_product.price * QUANTITY
    ) == (
        check_total_price_product - check_product.price * QUANTITY_BEFORE
    ), 'При изменение не изменилась общая сумма продукта.'


@pytest.mark.django_db
def test_delete_cart(authenticated_api_client, products, product):
    """Проверка delete запроса к корзине."""
    api_client, user = authenticated_api_client
    cart = Cart.objects.get(user=user)
    CartProduct.objects.create(
            cart=cart,
            product=product,
            quantity=1,
    )
    check_number = len(CartProduct.objects.filter(cart=cart))
    response = api_client.delete(reverse('cart-actions'))

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert len(CartProduct.objects.filter(cart=cart)) == 0, (
        'Корзина не пуста, после удаления'
    )
    assert len(CartProduct.objects.filter(cart=cart)) != check_number, (
        'Корзина не была наполнена перед тестом.'
    )
