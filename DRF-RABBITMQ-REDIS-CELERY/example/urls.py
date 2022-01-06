from django.urls.conf import include
from rest_framework import routers, viewsets
from rest_framework.urls import path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

router.register('tags', views.TagViewSet, basename='tag')

urlpatterns = [
    path('books/', views.BookList.as_view()),
    path('books/<int:pk>/', views.BookDetail.as_view()),

    path('authors/', views.AuthorAPIView.as_view()),
    path('authors/<int:id>/', views.AuthorAPIView.as_view()),
    path('categories/',
         views.CategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('categories/<int:id>/',
         views.CategoryViewSet.as_view(
             {
                 'get': 'retrieve',
                 'put': 'update',
                 'patch': 'partial_update',
                 'delete': 'destroy',
             })),
    path('', include(router.urls))
]
