from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=60)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Property(models.Model):
    name = models.CharField(max_length=60)
    type = models.CharField(max_length=60)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'properties'

    def __str__(self):
        return self.name


class PropertyValue(models.Model):
    name = models.CharField(max_length=60)
    value = models.TextField()
    property = models.ForeignKey(
        Property,  on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class GroupProperty(models.Model):
    group = models.CharField(max_length=60)
    category = models.ForeignKey(
        Category,  on_delete=models.CASCADE)
    properties = models.ManyToManyField(
        Property)

    class Meta:
        verbose_name_plural = 'group properties'

    def __str__(self):
        return self.group


class Product(models.Model):
    name = models.CharField(max_length=60)
    price = models.DecimalField(
        decimal_places=2, max_digits=17, default=0, null=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category, null=True,  on_delete=models.SET_NULL)
    brand = models.ForeignKey(
        Brand, null=True,  on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class ProductProperty(models.Model):
    value = models.TextField(null=True, blank=True)
    product = models.ForeignKey(
        Product,  on_delete=models.CASCADE)
    property = models.ForeignKey(
        Property,  on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'product properties'

    def __str__(self):
        return "{} - {}".format(self.product.name,  self.property.name)
