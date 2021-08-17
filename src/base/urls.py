from django.urls import path

from .views import RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView

app_name = 'base'
urlpatterns = [
    path('auth/user/', UserRetrieveUpdateAPIView.as_view()),
    path('auth/register/', RegistrationAPIView.as_view()),
    path('auth/login/', LoginAPIView.as_view()),

]
