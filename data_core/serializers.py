from rest_framework import serializers
from .models import Product, ProductImage
from taggit.serializers import (TagListSerializerField, TaggitSerializer)
from taggit.models import Tag

class ProductSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    class Meta:
        model = Product
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'