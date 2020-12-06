from django.contrib import admin
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.orders import Order


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
