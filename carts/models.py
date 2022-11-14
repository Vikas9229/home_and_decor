from django.db import models
from accounts.models import Account
from store.models import Product

# Create your models here.
class Cart(models.Model):
    cart_id=models.CharField(max_length=100)
    date_added=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,null=True,blank=True)
    variations=models.ManyToManyField('Variation',blank=True)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)
    user=models.ForeignKey(Account,on_delete=models.CASCADE,null=True,blank=True)

    def __unicode__(self):
        return self.product

    def sub_total(self):
        return self.product.price*self.quantity

variation_category_choice=(
    ('color','color'),
    ('size','size'),
)

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color',is_active=True)

    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size',is_active=True)

class Variation(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category=models.CharField(max_length=100,choices=variation_category_choice)
    variation_value=models.CharField(max_length=200)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now=True)

    objects=VariationManager()
    def __unicode__(self):
        return self.product

    def __str__(self):
        return self.variation_value