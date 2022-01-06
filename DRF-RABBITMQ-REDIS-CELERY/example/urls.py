from rest_framework.urls import path
from . import views

urlpatterns = [
    path('books/', views.BookList.as_view()),
    path('books/<int:pk>/', views.BookDetail.as_view()),
    path('authors/', views.AuthorAPIView.as_view()),
    path('authors/<int:id>/', views.AuthorAPIView.as_view()),
]
