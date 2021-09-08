from django.urls import path

from . import views

app_name = 'base'
urlpatterns = [
    path('auth/user/', views.UserRetrieveUpdateAPIView.as_view()),
    path('auth/register/', views.RegistrationAPIView.as_view()),
    path('auth/login/', views.LoginAPIView.as_view()),
    path('auth/confirm/', views.ConfirmEmailAPIView.as_view()),

]
