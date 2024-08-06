from django.db import models
from vendor.models import Vendor

# Create your models here.

class Category(models.Model):
    vendor = models.ForeignKey(Vendor,related_name="vendors",on_delete=models.CASCADE)
    category_name = models.CharField(max_length = 100)
    slug = models.SlugField(max_length = 100)
    description = models.CharField(max_length = 200)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now_add = True)

    def __str__(self):
        return self.category_name


class FoodItem(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)   
    category = models.ForeignKey(Category, on_delete =models.CASCADE,related_name='fooditems')
    food_name = models.CharField(max_length = 200) 
    slug = models.SlugField(max_length = 200)
    description = models.CharField(max_length = 200)
    images = models.ImageField(upload_to='fooodimage', blank = True)
    price = models.IntegerField()
    is_available = models.BooleanField(default = False)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now_add = True)

    def __str__(self):
        return self.food_name






