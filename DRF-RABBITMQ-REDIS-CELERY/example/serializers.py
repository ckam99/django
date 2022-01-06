from django.db.models import fields
from rest_framework import serializers
from .models import Book, Author, Tag, Category
from core.mixins.queryset import EagerLoadingMixin


class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)

    class Meta:
        fields = ['id', 'name']

    def create(self, validated_data):
        return Author.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class BookSerializer(serializers.ModelSerializer, EagerLoadingMixin):
    author = AuthorSerializer(many=False, read_only=True)
    author_id = serializers.IntegerField(required=False, write_only=True)
    prefetch_related_fields = ('author', )

    class Meta:
        model = Book
        fields = ['id', 'title', 'description',
                  'published', 'author', 'author_id']


class AuthorDetailSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
