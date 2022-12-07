from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from carts.models import Cart,CartItem,Product
from carts.views import _cart_id
from .models import Order,OrderProduct,Payment
import datetime
import json
from .import views
from django.template.loader import render_to_string
# Create your views here.
@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)

@login_required(login_url="login")
def place_order(request,total=0,quantity=0):
    current_user=request.user
    cart_items=CartItem.objects.filter(user=current_user)
    cart_count=cart_items.count()
    if cart_count<=0:
        return redirect('store')
    tax=0
    grand_total=0
    for cart_item in cart_items:
        total=total+(cart_item.product.price*cart_item.quantity)
        quantity=quantity+cart_item.quantity
    tax=(total*8)/100
    grand_total=total+tax
    if request.method=="POST":
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        address_line1=request.POST.get('address_line_1')
        address_line2=request.POST.get('address_line_2')
        country=request.POST.get('country')
        city=request.POST.get('city')
        state=request.POST.get('state')
        order_note=request.POST.get('order_note')
        order_total=grand_total
        tax=tax
        ip=request.META.get('REMOTE_ADDR')
        
        current_data=Order(user=current_user,first_name=first_name,last_name=last_name,phone=phone,email=email,address_line_1=address_line1,address_line_2=address_line2,country=country,city=city,state=state,order_note=order_note,order_total=order_total,tax=tax,ip=ip)  
        current_data.save()
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d')) 
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr,mt,dt)
        current_date = d.strftime("%Y%m%d") #20210305
        order_number = current_date + str(current_data.id)
        current_data.order_number=order_number
        current_data.save()
        order=Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
        context={
            'order':order,
            'cart_items':cart_items,
            'total':total,
            'tax':tax,
            'grand_total':grand_total
        }
        return render(request,'orders/payments.html',context)
    else:
        return redirect('checkout')


def razorpay(request,id):
    import razorpay
    order_details = Order.objects.get(id=id)
    client = razorpay.Client(auth=("rzp_test_B9st9Hrr0Tp8ZA", "Ve68z22EhYIf3jOBrBo3o8Th"))
    data = { "amount": int(order_details.order_total)*100, "currency": "INR", "receipt": "Itinerary Buddy" }
    payment_amount=data["amount"]
    payment = client.order.create(data=data)
    razorpay_order_ID = payment['id']
    amount = data.get('amount')
    name = {order_details.email}

    payment  = Payment(
    user=request.user,
    payment_id=razorpay_order_ID,
    amount_paid=order_details.order_total,
    status=True,
    created_at=datetime.datetime.now
    )
    payment.save()

    order=Order.objects.get(user=request.user,is_ordered=False,id=order_details.id)
    order.payment=payment
    order.save()

    cart_items=CartItem.objects.filter(user=request.user)
   
    for item in cart_items:
        orderproduct=OrderProduct()
        orderproduct.order_id=order.id
        orderproduct.payment=payment
        orderproduct.user_id=request.user.id
        orderproduct.product_id=item.product_id
        orderproduct.product_price=item.product.price
        orderproduct.ordered=True
        orderproduct.save()

        orderproduct=OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.save()
    context = {'amount':amount,'name':name,'razorpay_order_ID':razorpay_order_ID,'order_details':order_details}
    return render(request,"accounts/razorpay.html",context)

def paymentdone(request,id):
    CartItem.objects.filter(user=request.user).delete()
    order=Order.objects.filter(id=id).update(is_ordered=True)
    return render(request,'orders/order_complete.html')




    
# def payments(request):
#     body=json.loads(request.body)
#     print(body)
#     order=Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
#     print(order)
#     payment=Payment(
#         user=request.user,
#         payment_id=body['transID'],
#         payment_method=body['payment_method'],
#         amount_paid=order.order_total,
#         status=body['status'],
#     )
#     print(payment)
#     payment.save()
#     order.payment=payment
#     order.is_ordered=True
#     order.save()
#     cart_items=CartItem.objects.filter(user=request.user)
#     for item in cart_items:
#         orderproduct=OrderProduct()
#         orderproduct.order_id=order.id
#         orderproduct.payment=payment
#         orderproduct.user_id=request.user.id
#         orderproduct.product_id=item.product.id
#         orderproduct.quantity=item.quantity
#         orderproduct.product_price=item.product.price
#         orderproduct.ordered=True
#         orderproduct.save()
        
#         cart_item=CartItem.objects.get(id=item.id)
#         product_variation=cart_item.variations.all()
#         orderproduct=OrderProduct.objects.get(id=orderproduct.id)
#         orderproduct.variations.set(product_variation)
#         orderproduct.save()
        
#         product=Product.objects.get(id=item.product_id)
#         product.stock=product.stock-item.quantity
#         product.save()
        
#         CartItem.objects.filter(user=request.user).delete()

#         mail_subject='Thank you for ur order !'
#         message=render_to_string('orders/order_received_email.html',{
#             'user':request.user,
#             'order':order,
#         })
#         to_mail=request.user.email
#         print(to_mail)
#         send_email=EmailMessage(mail_subject,message,to=[to_mail])
#         send_email.send()
        
#         data={
#             'order_number':order.order_number,
#             'transID':payment.payment_id,
#         }
#         return JsonResponse(data)
        
#     return render(request,'orders/payments.html')

# def order_complete(request):
#     order_number=request.GET.get('order_number')
#     transID=request.GET.get('payment_id')
#     try:
#         order=Order.objects.get(order_number=order_number,is_ordered=True)
#         ordered_products=OrderProduct.objects.filter(order_id=order.id)

#         subtotal=0
#         for i in ordered_products:
#             subtotal=subtotal+i.product_price*i.quantity
#         payment=Payment.objects.get(payment_id=transID)
#         context={
            
#             'order':order,
#             'ordered_products':ordered_products,
#             'order_number':order.order_number,
#             'transID':payment.payment_id,
#             'payment':payment,
#             'subtotal':subtotal,

#         }
#         return render(request,'orders/order_complete.html',context)
#     except (Payment.DoesNotExist,Order.DoesNotExist):
#         return redirect('home')



# def razorpay(request,id):
    
#    import razorpay
#    order_details = Order.objects.get(id=id)
#    print(order_details)
#    client = razorpay.Client(auth=("rzp_test_B9st9Hrr0Tp8ZA", "Ve68z22EhYIf3jOBrBo3o8Th"))

#    data = { "amount": int(order_details.order_total) * 100, "currency": "INR", "receipt": "" }
#    print(data)
#    payment_amount=data["amount"]
#    payment = client.order.create(data=data)
#    razorpay_order_ID = payment['id']
#    amount = (data.get('amount'))
#    print(amount)
#    name = {order_details.email}
#    context = {'amount':amount,'name':name,'razorpay_order_ID':razorpay_order_ID,'order_details':order_details}

#    payment_db  = Payment(user=request.user,payment_id=razorpay_order_ID,amount_paid=order_details.order_total,status=True,created_at=datetime.datetime.now)
#    payment_db.save()
#    order=Order.objects.get(user=request.user,is_ordered=False,id=order_details.id)
#    order.payment=payment_db
#    order.save()
#    cart_items=CartItem.objects.filter(user=request.user)
#    for item in cart_items:
#         orderproduct=OrderProduct()
#         orderproduct.order_id=order.id
#         orderproduct.payment=payment_db
#         orderproduct.user_id=request.user.id
#         orderproduct.product_id=item.product_id
#         orderproduct.product_price=item.product.price
#         orderproduct.ordered=True
#         orderproduct.save() 
#         cart_item=CartItem.objects.get(id=item.id)
#         orderproduct=OrderProduct.objects.get(id=orderproduct.id)
#         orderproduct.save()
#         cart_data = CartItem.objects.filter(user=request.user).delete()

#         return render(request,"accounts/razorpay.html",context)


# def paymentdone(request,id):
#     try:
#         order_number=request.GET.get(id)
#         transID=request.GET.get(id)
#         print(order_number)
#         print(transID)
#         order=Order.objects.get(order_number=order_number,is_ordered=True)
#         ordered_products=OrderProduct.objects.filter(order_id=order.id)

#         subtotal=0
#         for i in ordered_products:
#             subtotal=subtotal+i.product_price*i.quantity
#             payment=Payment.objects.get(payment_id=transID)
#         context={
                
#             'order':order,
#             'ordered_products':ordered_products,
#             'order_number':order.order_id,
#             'transID':payment.payment_id,
#             'payment':payment,
#             'subtotal':subtotal,

#         }
#         return render(request,'orders/order_complete.html',context)
#     except (Payment.DoesNotExist,Order.DoesNotExist):
#         return redirect('home')
