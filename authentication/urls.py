from django.urls import path
from .views import RegisterView, LoginView, CurrentUserView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('me', CurrentUserView.as_view()),
]
