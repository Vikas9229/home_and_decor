from django.contrib import admin
from .models import Cart,CartItem,Variation

# Register your models here.
class VariationAdmin(admin.ModelAdmin):
    list_display=['product','variation_category','variation_value','is_active','created_date']

class CartAdmin(admin.ModelAdmin):
    list_display=['cart_id','date_added']

class CartItemAdmin(admin.ModelAdmin):
    list_display=['product','cart','quantity','is_active']

admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem,CartItemAdmin)
admin.site.register(Variation,VariationAdmin)