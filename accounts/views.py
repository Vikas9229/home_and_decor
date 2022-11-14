from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegistrationForm,UserProfileForm,UserForm
from .models import Account,UserProfile
from django.contrib import messages,auth
from carts.models import CartItem,Cart
from orders.models import Order
from carts.views import _cart_id

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method=="POST":
        form=RegistrationForm(request.POST)
        print(form)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            phone_number=form.cleaned_data['phone_number']
            username=email.split("@")[0]
            user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username)
            user.phone_number=phone_number
            user.save()
            messages.success(request,"Registration successful... we have sent an email please check your email id ")
            current_site=get_current_site(request)
            mail_subject="Please activate your account"
            message=render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            return redirect('login')
    else:
    
        form=RegistrationForm()       
    context={
         'form':form,    
    }

    return render(request,'accounts/register.html',context)

def login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            try:
                cart=Cart.objects.get(cart_id=_cart_id(request))
                cart_item_exists=CartItem.objects.filter(cart=cart).exists()
                if cart_item_exists:
                    cart_item=CartItem.objects.filter(cart=cart)
                    product_variation=[]
                    for item in cart_item:
                        variation=item.variations.all()
                        product_variation.append(list(variation))
                    cart_item=CartItem.objects.filter(user=user)
                    ex_var_list=[]
                    id=[]
                    for item in cart_item:
                        existing_variation=item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                    
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index=ex_var_list.index(pr)
                            item_id=id[index]
                            item=CartItem.objects.get(id=item_id)
                            item.quantity+=1
                            item.user=user
                            item.save()
                        else:
                            cart_item=CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user=user
                                item.save()
           
            except:
                pass
            auth.login(request,user)
            messages.success(request,"login successful")
            return redirect('home')
        else:
            messages.error(request,"Please check your credentials")
            return redirect('login')

    return render(request,'accounts/login.html')

def activate(request,uidb64,token):
    uid=urlsafe_base64_decode(uidb64).decode()
    user=Account._default_manager.get(pk=uid)
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,"Congratulations your account is activated")
        return redirect('login')
    else:
        messages.error("Invalid link")
        return redirect('register')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,"You are succcessfully logged out")
    return redirect('login')

def forgotPassword(request):
    if request.method=='POST':
        email=request.POST.get('email')
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__exact=email)
            current_site=get_current_site(request)
            mail_subject="Reset your password"
            message=render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),

                'token':default_token_generator.make_token(user),
            })
            to_email=email
            send_mail=EmailMessage(mail_subject,message,to=[to_email])
            send_mail.send()
            messages.success(request,'Password reset email has been sent to ur email address')
            return redirect('forgotPassword')
        else:
            messages.error(request,'Account does not exist')
            return redirect('forgotPassword')


    return render(request,'accounts/forgotPassword.html')

def reset_password_validate(request,uidb64,token):
    uid=urlsafe_base64_decode(uidb64).decode()#uid=1
    user=Account._default_manager.get(pk=uid)
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,"pleas reset ur password")
        return redirect('resetPassword')
    else:
        messages.error(request,'this link has been expired')
        return redirect('login')

def resetPassword(request):
    if request.method=="POST":
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        if password==confirm_password:
            uid=request.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'password has been reset')
            return redirect('login')
        else:
            messages.error(request,'password do not match')
            return redirect('resetPassword')
    return render(request,'accounts/resetPassword.html')

@login_required(login_url="login")
def dashboard(request):
    user=request.user
    print(user)
    orders=Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered=True)
    order_count=orders.count()
    print(order_count)
    # userprofile=UserProfile.objects.get(user=request.user.id)
    context={
        'order_count':order_count,
        # 'userprofile':userprofile,
    }
    return render(request,'accounts/dashboard.html',context)
@login_required(login_url="login")
def my_orders(request):
    orders=Order.objects.filter(user=request.user,is_ordered=True)
    context={
        'orders':orders,
    }
    return render(request,'accounts/my_orders.html',context)

@login_required(login_url="login")
def edit_profile(request):
    # userprofile=get_object_or_404(UserProfile,user=request.user)
    userprofile=UserProfile.objects.get(users=request.user)
    if request.method=="POST":#jab user form ko edit karega
        user_form=UserForm(request.POST,instance=request.user)
        profile_form=UserProfileForm(request.POST,instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,"Your Profile has been updated")
            return redirect('edit_profile')
    else:#sirf user ka data laakar rakh dega
        user_form=UserForm(instance=request.user)
        print(user_form)
        profile_form=UserProfileForm(instance=userprofile)
        print(profile_form)
    context={
        'user_form':user_form,
        'profile_form':profile_form,
        'userprofile':userprofile
    }
    return render(request,'accounts/edit_profile.html',context)


@login_required(login_url="login")
def change_password(request):
    if request.method=='POST':
        current_password=request.POST['current_password']
        new_password=request.POST['new_password']
        confirm_password=request.POST['confirm_password']

        user=Account.objects.get(username=request.user.username)

        if new_password==confirm_password:#jab new aur confirm match karega
            success=user.check_password(current_password)
            if success:#current password jab match karega
                user.set_password(new_password)
                user.save()
                messages.success(request,"Your password has been updated")
                return redirect('change_password')
            else:#current password jab match nahi karega
                messages.error(request,"please enter valid password")
                return redirect('change_password')
        else:#jab new aur confirm match nahi kartega
            messages.error(request,'password do not mach')
            return redirect('change_password')
    return render(request,'accounts/change_password.html')