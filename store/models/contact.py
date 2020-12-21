from django.db import models

class ContactModel(models.Model):
    fname = models.CharField(max_length=10)
    lname = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    comments = models.TextField(max_length=500)
    def __str__(self):
        return self.fname+" "+self.lname

    
    def shortComments(self):
        mycomments = self.comments[:30]
        return mycomments