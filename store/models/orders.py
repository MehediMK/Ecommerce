from django.db import models
from .product import Product
from .customer import Customer
import datetime

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    address = models.CharField(max_length=150,default='')
    phone = models.CharField(max_length=15,default='')
    date = models.DateField(default = datetime.datetime.today)

    def __str__(self):
        return self.address
    


    def placeOrder(self):
        self.save()
    