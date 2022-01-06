from rest_framework import generics, mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import HttpRequest
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .serializers import (
    BookSerializer,
    AuthorSerializer,
    AuthorDetailSerializer,
    CategorySerializer,
    TagSerializer
)
from .models import Book, Author, Category, Tag


class AuthorAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'id'

    def get(self, request: HttpRequest, id: int = None):
        if id:
            self.queryset = self.queryset.prefetch_related('books')
            self.serializer_class = AuthorDetailSerializer
            return self.retrieve(request, id)
        return self.list(request)

    def post(self, request: HttpRequest):
        return self.create(request)

    def put(self, request: HttpRequest, id: int = None):
        return self.update(request, id)

    def delete(self, request: HttpRequest, id: int = None):
        return self.destroy(request, id)


class BookList(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()


class CategoryViewSet(viewsets.ViewSet):

    def get_object(self, pk: int) -> Category:
        ''' get object '''
        return generics.get_object_or_404(Category, pk=pk)

    def update_object(self, request: HttpRequest, pk: int, is_partial: bool = False):
        ''' Shared update method  To avoid to repeat your-self  '''
        serializer = CategorySerializer(
            self.get_object(pk), data=request.data, partial=is_partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer

    def list(self, request: HttpRequest):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request: HttpRequest):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request: HttpRequest, id: int):
        serializer = CategorySerializer(self.get_object(pk=id))
        return Response(serializer.data)

    def update(self, request: HttpRequest, *args, **kwargs):
        serializer = self.update_object(request, pk=kwargs.get('id'))
        return Response(serializer.data)

    def partial_update(self, request: HttpRequest, *args, **kwargs):
        serializer = self.update_object(
            request, pk=kwargs.get('id'), is_partial=True)
        return Response(serializer.data)

    def destroy(self, request: HttpRequest, id: int):
        instance = self.get_object(pk=id)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(methods=['GET'], detail=True)
    def books(self, request: HttpRequest, pk=None):
        books = Book.objects.filter(tags__in=[pk])
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
