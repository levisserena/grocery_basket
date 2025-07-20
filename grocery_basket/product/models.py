from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from core.constants import LENGTH_SLUG, LENGTH_TEXT_LONG
from core.mixins import DateAutoMixin


class BaseProductBase(models.Model):

    name = models.CharField(
        verbose_name='Наименование',
        max_length=LENGTH_TEXT_LONG,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=LENGTH_SLUG,
        unique=True,
        help_text='Уникальный идентификатор, '
        'разрешены символы латиницы, цифры, дефис и подчёркивание.',
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.__class__.__name__}(slug={self.slug}, name={self.name})'


class Category(BaseProductBase, DateAutoMixin):

    image = models.ImageField(
        verbose_name='Наименование',
        upload_to='category/',
        null=True,
        default=None,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subcategory(BaseProductBase, DateAutoMixin):

    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='subcategory/',
        null=True,
        default=None,
    )
    category = models.ForeignKey(
        Category,
        related_name='subcategory',
        verbose_name='Категория',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return f'{self.category}: {self.name}'


class Product(BaseProductBase, DateAutoMixin):

    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='product/',
        null=True,
        default=None,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
    )
    subcategory = models.ForeignKey(
        Subcategory,
        verbose_name='Подкатегория',
        on_delete=models.CASCADE,
    )
    price = models.DecimalField(
        verbose_name='Цена',
        null=True,
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(
                0, message='Значение не может быть меньше 0'
            ),
        ],
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(100, 100)],
        format='JPEG',
        options={'quality': 60}
    )
    image_medium = ImageSpecField(
        source='image',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 80}
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def clean(self):
        """Дополнительная проверка.

        Проверит, что при создании категория и подкатегория связаны друг с
        другом.
        """
        super().clean()
        if self.subcategory.category != self.category:
            raise ValidationError(
                'Выбранная подкатегория не принадлежит выбранной категории'
            )

    def save(self, *args, **kwargs):
        """Перед сохранением вызовет метод clean."""
        self.full_clean()
        super().save(*args, **kwargs)
