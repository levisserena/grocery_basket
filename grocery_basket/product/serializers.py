from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Category, Product, Subcategory


class SubcategorySerializer(ModelSerializer):

    class Meta:
        model = Subcategory
        fields = 'id', 'name', 'slug', 'image'


class CategorySerializer(ModelSerializer):

    subcategory = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = 'id', 'name', 'slug', 'image', 'subcategory'


class ProductSerializer(ModelSerializer):

    image_thumbnail = SerializerMethodField()
    image_medium = SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'slug',
            'price',
            'category',
            'subcategory',
            'image',
            'image_thumbnail',
            'image_medium',
        )

    def get_image_thumbnail(self, obj):
        """Обрабатывает поле image_thumbnail"""
        return obj.image_thumbnail.url if obj.image_thumbnail else None

    def get_image_medium(self, obj):
        """Обрабатывает поле image_thumbnail"""
        return obj.image_medium.url if obj.image_medium else None
