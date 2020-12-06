from django.db import models
from django.shortcuts import redirect

class Customer(models.Model):
    first_name = models.CharField(max_length = 25)
    last_name = models.CharField(max_length = 25)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def __str__(self):
        return self.first_name+" - "+self.email
    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

    def register(self):
        self.save()

    def isExits(self):
        if Customer.objects.filter(email = self.email):
            return True
        else:
            return False
