from django.contrib import admin
from shop.models import *

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(SubCategory)
admin.site.register(Attribute)
admin.site.register(Product)
admin.site.register(ProductAttributeValue)

