from django.db import models
from category.models import Category
from django.urls import reverse

from accounts.models import Account


# Create your models here.
class Product(models.Model):
    product_name=models.CharField(max_length=100)
    images=models.ImageField(upload_to="photos/product")
    description=models.TextField(max_length=200)
    slug=models.SlugField(max_length=100)
    price=models.IntegerField()
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    upload_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])

    def __str__(self):
        return self.product_name

class ReviewRating(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    subject=models.CharField(max_length=150,blank=True)
    review=models.TextField(max_length=600,blank=True)
    rating=models.FloatField()
    ip=models.CharField(max_length=200,blank=True)
    status=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
