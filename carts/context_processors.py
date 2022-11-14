from .models import Cart,CartItem
from .views import _cart_id
def counter(request):
    if 'carts/carts' in request.path:
        try:
            cart_count=0
            if request.user.is_authenticated:
                  cart_items=CartItem.objects.filter(user=request.user,is_active=True)

            else:
                cart=Cart.objects.get(cart_id=_cart_id(request))
                cart_items=CartItem.objects.filter(cart=cart,is_active=True)
            for cart_item in cart_items:
                cart_count=cart_count+cart_item.quantity
            return dict(cart_count=cart_count)
        except Cart.DoesNotExist:
            cart_count=0
    else:
        return {}
        