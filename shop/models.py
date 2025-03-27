from django.db import models
from django.core.exceptions import ValidationError
from django_jalali.db import models as jmodels
from account.models import CustomUser

class Category(models.Model):
    objects = jmodels.jManager()

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)
    meta_description = models.TextField(max_length=160)
    datetime_created = jmodels.jDateTimeField(auto_now_add=True)
    datetime_modified = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        ordering = ["-datetime_created"]

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=150)
    fa_name = models.CharField(max_length=150)
    url = models.URLField(null=True, blank=True, max_length=150)
    brand_logo = models.ImageField(upload_to='brand_logos/', null=True, blank=True)

    class Meta:
        verbose_name_plural = "brands"

    def __str__(self):
        return self.fa_name

class SubCategory(models.Model):
    objects = jmodels.jManager()

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="sub_categories")
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)
    meta_description = models.TextField(max_length=160)
    datetime_created = jmodels.jDateTimeField(auto_now_add=True)
    datetime_modified = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        ordering = ["-datetime_created"]

    def __str__(self):
        return f"{self.name} ({self.category.name if self.category else 'No Category'})"

class Attribute(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="attributes")
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ["category__datetime_created"]

    def __str__(self):
        return f"{self.name} ({self.category.name if self.category else 'No Category'})"

class Product(models.Model):
    objects = jmodels.jManager()

    owner = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=100)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, related_name="products")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, related_name="products")
    count = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    off_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_off = models.BooleanField(default=False)
    is_stock = models.BooleanField(default=False)
    description = models.TextField(default="")
    meta_description = models.TextField(max_length=160)
    datetime_created = jmodels.jDateTimeField(auto_now_add=True)
    datetime_modified = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        ordering = ["-datetime_created"]

    def __str__(self):
        status_icon = "🟢" if self.is_stock else "🔴"
        return f"{status_icon} {self.name} ({self.sub_category.category.name if self.sub_category else 'No SubCategory'})"

    def clean(self):
        if self.off_price >= self.price:
            raise ValidationError("Discount price must be less than the original price.")

class ProductAttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name="product_values")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_values")
    value = models.CharField(max_length=250)
