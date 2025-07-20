from django.contrib.admin import ModelAdmin, register, site
from django.utils.safestring import mark_safe

from .models import Category, Product, Subcategory

site.site_title = 'Администрирование.'
site.site_header = 'Администрирование'


class BaseProductAdmin(ModelAdmin):

    def get_html_image(self, obj):
        """Возвращает превью изображения"""
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width=70>')
        return 'Нет изображения'

    get_html_image.short_description = 'Превью изображения'  # type: ignore


@register(Category)
class CategoryAdmin(BaseProductAdmin):

    fields = ('slug', 'name', 'image', 'get_html_image')
    list_display = 'id', 'name', 'slug'
    list_display_links = 'id', 'name', 'slug'
    search_fields = 'name', 'slug'
    readonly_fields = ('get_html_image',)


@register(Subcategory)
class SubcategoryAdmin(BaseProductAdmin):

    fields = 'slug', 'name', 'category', 'image', 'get_html_image'
    list_display = 'id', 'name', 'slug', 'category'
    list_display_links = 'id', 'name', 'slug'
    search_fields = 'name', 'slug', 'category'
    readonly_fields = ('get_html_image',)


@register(Product)
class ProductAdmin(BaseProductAdmin):

    fields = (
        'slug',
        'name',
        'category',
        'subcategory',
        'price',
        'image',
        'get_html_image',
    )
    list_display = 'id', 'name', 'slug', 'category', 'subcategory', 'price'
    list_display_links = 'id', 'name', 'slug'
    search_fields = 'name', 'slug', 'category'
    readonly_fields = ('get_html_image',)
    list_editable = ('price',)
