from django.db import models
from .category import Category

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    unit = models.CharField(max_length = 15,blank=True)
    description = models.TextField(max_length=1000,null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    image = models.ImageField(upload_to = 'products/')


    def __str__(self):
        return self.name

    @staticmethod
    def get_product_by_id(ids):
        return Product.objects.filter(id__in = ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(categoryid):
        if categoryid:
            return Product.objects.filter(category = categoryid)
        else:
            return Product.objects.all()
    