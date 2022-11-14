from django.contrib import admin

from .models import Order,OrderProduct,Payment

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display=['id','first_name','last_name','order_number']


class OrderProductAdmin(admin.ModelAdmin):
    list_display=['quantity','product_price','ordered']


class PaymentAdmin(admin.ModelAdmin):
    list_display=['payment_id','status','amount_paid']


admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)
admin.site.register(Payment,PaymentAdmin)