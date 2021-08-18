from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('base.urls', namespace="base")),
    path('', TemplateView.as_view(template_name='index.html'))
]

if not settings.DEBUG:
    handler404 = "base.views.handler404"
