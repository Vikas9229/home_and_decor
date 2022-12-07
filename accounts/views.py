from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegistrationForm,UserProfileForm,UserForm,DesignerForm
from .models import Account,UserProfile,Designer
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


from http.client import HTTPResponse
from rest_framework.response import Response
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login,logout
from rest_framework.authtoken.models import Token
import rest_framework.status as status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt 
import requests
from datetime import datetime
from django.conf import settings
from django.contrib import messages
from employee.models import CustomUser as User
from django.urls import reverse

from employee.serializer import UserSerializer

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

def designer(request):
    if request.method=="POST":
        form=DesignerForm(request.POST)
        print(form)
        # if form.is_valid():
        first_name=form.cleaned_data['first_name']
        last_name=form.cleaned_data['last_name']
        email=form.cleaned_data['email']
        password=form.cleaned_data['password']
        phone_number=form.cleaned_data['phone_number']
        username=email.split("@")[0]
        user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username)
        user.is_architect = False
        user.phone_number=phone_number
        user.save()
        current_user = Account.objects.get(id=user.id)
        designer_user = Designer(user=current_user).save()
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
    
        form=DesignerForm()       
    context={
         'form':form,    
    }

    return render(request,'accounts/designer.html',context)

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


def loginViewForHtml(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            auth_login(request,user)
            token = Token.objects.get(user__username = username)
            user_data = User.objects.get(username=username)
            data = {'name':user_data.get_full_name(),'token':token.key,'id':user_data.id}
            return redirect('home')
        return Response(data='Invalid data')
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def logoutView(request):
    logout(request)
    return Response(data="Successfully Logout!!")


def google_login(request):
    redirect_uri = "%s://%s%s" % (
        request.scheme, request.get_host(), reverse('google_login')
    )
    if('code' in request.GET):
        params = {
            'grant_type': 'authorization_code',
            'code': request.GET.get('code'),
            'redirect_uri': redirect_uri,
            'client_id': settings.GP_CLIENT_ID,
            'client_secret': settings.GP_CLIENT_SECRET
        }
        url = 'https://accounts.google.com/o/oauth2/token'
        response = requests.post(url, data=params)
        url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        access_token = response.json().get('access_token')
        response = requests.get(url, params={'access_token': access_token})
        user_data = response.json()
        email = user_data.get('email')
        if email:
            user, _ = User.objects.get_or_create(email=email, username=email)
            gender = user_data.get('gender', '').lower()
            if gender == 'male':
                gender = 'M'
            elif gender == 'female':
                gender = 'F'
            else:
                gender = 'O'
            data = {
                'first_name': user_data.get('name', '').split()[0],
                'last_name': user_data.get('family_name'),
                'google_avatar': user_data.get('picture'),
                'gender': gender,
                'is_active': True
            }
            user.__dict__.update(data)
            user.save()
            user.backend = settings.AUTHENTICATION_BACKENDS[0]
            auth_login(request, user)
            return render(request,'home.html')
        else:
            messages.error(
                request,
                'Unable to login with Gmail Please try again'
            )
        return redirect('/')
    else:
        url = "https://accounts.google.com/o/oauth2/auth?client_id=%s&response_type=code&scope=%s&redirect_uri=%s&state=google"
        scope = [
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email"
        ]
        scope = " ".join(scope)
        url = url % (settings.GP_CLIENT_ID, scope, redirect_uri)
        return redirect(url)

def loginpage(request):
    return render(request,'login.html')
def Signuppage(request):
    return render(request,'register.html')


def SignupapiForHtml(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('f_name')
        last_name = request.POST.get('l_name')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name)
        user.save()
        userdata = User.objects.get(username=username)
        user_ser = UserSerializer(userdata).data
        return redirect('login-page')
    