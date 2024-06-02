from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Category (models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length = 255)

    def __str__(self):
        return self.title

class MenuItem(models.Model):
    title = models.SlugField()
    price = models.CharField(max_length = 255)
    inventory = models.DecimalField(max_digits=6,decimal_places=2)
    category = models.ForeignKey(Category,on_delete = models.PROTECT,default = 1)
    def __str__(self):
        return self.title
    
class order_list(models.Model):
    order = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    time = models.TimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    phone = models.TextField(max_length=14)
    useraddress = models.TextField(max_length=500)
    quantity = models.IntegerField(default=0)
    email = models.EmailField()

class Cart(models.Model):
    item = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

class Likes(models.Model):
    item = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    
    
class Comments(models.Model):
    comment = models.TextField(max_length=800)
    item = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    

    