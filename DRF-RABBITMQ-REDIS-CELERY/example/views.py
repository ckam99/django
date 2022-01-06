from rest_framework import generics, mixins
from django.http import HttpRequest
from .serializers import BookSerializer, AuthorSerializer, AuthorDetailSerializer
from .models import Book, Author


class AuthorAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'id'

    def get_serializer_class(self):
        return super().get_serializer_class()

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
