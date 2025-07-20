from django.urls import path

from .views import CartViewSet

urlpatterns = [
    path(
        route='cart/',
        view=CartViewSet.as_view({
            'get': 'get',
            'post': 'create',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }),
        name='cart-actions',
    )
]
