from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Brand)
admin.site.register(models.Category)
admin.site.register(models.Property)
admin.site.register(models.PropertyValue)
admin.site.register(models.GroupProperty)
admin.site.register(models.Product)
admin.site.register(models.ProductProperty)
