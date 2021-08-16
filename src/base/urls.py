from django.urls import path

from .views import RegistrationAPIView

app_name = 'base'
urlpatterns = [
    path('users/', RegistrationAPIView.as_view()),
]
