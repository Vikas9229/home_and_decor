from django.urls import path
from .import views

urlpatterns = [  
    path('',views.checkout,name='checkout'),
    path('place_order/',views.place_order,name='place_order'),
    path('payments/<int:id>/',views.razorpay,name='razorpay'),
    path('payment_done/<int:id>/',views.paymentdone,name='payment-done'),
    # path('order_complete/',views.order_complete,name='order_complete'),
]