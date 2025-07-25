# Generated by Django 5.2.3 on 2025-07-20 19:11

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('slug', models.SlugField(help_text='Уникальный идентификатор, разрешены символы латиницы, цифры, дефис и подчёркивание.', max_length=40, unique=True, verbose_name='Слаг')),
                ('image', models.ImageField(default=None, null=True, upload_to='category/', verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('slug', models.SlugField(help_text='Уникальный идентификатор, разрешены символы латиницы, цифры, дефис и подчёркивание.', max_length=40, unique=True, verbose_name='Слаг')),
                ('image', models.ImageField(default=None, null=True, upload_to='subcategory/', verbose_name='Изображение')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategory', to='product.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Подкатегория',
                'verbose_name_plural': 'Подкатегории',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('slug', models.SlugField(help_text='Уникальный идентификатор, разрешены символы латиницы, цифры, дефис и подчёркивание.', max_length=40, unique=True, verbose_name='Слаг')),
                ('image', models.ImageField(default=None, null=True, upload_to='product/', verbose_name='Изображение')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0, message='Значение не может быть меньше 0')], verbose_name='Цена')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.category', verbose_name='Категория')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.subcategory', verbose_name='Подкатегория')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
                'ordering': ['name'],
            },
        ),
    ]
