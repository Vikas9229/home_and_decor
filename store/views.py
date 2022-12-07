from django.shortcuts import render,redirect,HttpResponse
from .models import Product,Architects
from category.models import Category
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from .models import ReviewRating
from .forms import ReviewForm,ArchitectsForm
from django.core.mail import send_mail


# Create your views here.

def architects(request):
    # if request.method=="POST":
    #     pname=request.POST.get('pname')
    #     img=request.POST.get('img')
    #     descrp=request.POST.get('descrp')
    #     office=request.POST.get('office')
    #     email=request.POST.get('email')
    #     Product(product_name=pname,images=img,description=descrp,offi).save()
    architect=Architects.objects.all()
    print(architect)


    context={
        'architect':architect,
    }
       
       
    return render(request,'store/architects.html',context)



def architect_upload(request):
    if request.method == "POST":
        user=request.user
        # cname=request.POST['cname']
        # description=request.POST['desc']
        # address=request.POST['addr']
        # email=request.POST['email']
        # image=request.POST['image']
        # architect=Architects(company_name=cname,images=image,descript=description,email=email,office_add=address,user=user)
        # architect.save()
        form=ArchitectsForm(request.POST,  request.FILES)
        if form.is_valid():
            form.save()
        else:
            return HttpResponse(form.errors)
        
    return render(request,'store/architect_upload.html')

def architect_profile(request):
    profile=Architects.objects.filter(user=request.user)
    print(profile)
    context={
        'profile':profile
    }
    return render(request,'store/architects.html',context)

def contact(request):
    if request.method == "POST":
        message_name = request.POST['message_name']
        message_email = request.POST['message_email']
        message_number = request.POST['message_number']
        message_address = request.POST['message_address']
        message = request.POST['message']

        # send mail
        send_mail(
            'Inquiry from Customer',
            'message_name , message',
            'message_email',
            [request.user.email],
            fail_silently=False,
        )
        print

        return render(request,'store/contact.html')

    else:
        return render(request,'store/contact.html')

def store(request,category_slug=None):
    if category_slug!=None:
        categories=Category.objects.get(slug=category_slug)
        products=Product.objects.filter(category=categories)
        paginator=Paginator(products,10)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)

        product_count=products.count()
    else:
        products=Product.objects.filter(is_available=True)
        paginator=Paginator(products,10)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        product_count=products.count()
    

    context={
        'products':paged_products,
        'product_count':product_count,

    }
    return render(request,'store/store.html',context)

def product_detail(request,category_slug,product_slug):
    single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
    context={
        'single_product':single_product
    }
    return render(request,'store/product_detail.html',context)


def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET.get('keyword')
        if keyword:
            products=Product.objects.order_by("-upload_date").filter(Q(description__icontains=keyword)|Q (product_name__icontains=keyword))
            product_count=products.count()
            context={
                'products':products,
                'product_count':product_count,
            }
        else:
            return redirect('store')
    return render(request,'store/store.html',context)

def submit_review(request,product_id):
    url=request.META.get('HTTP_REFERER')
    if request.method=="POST":
        #yaha par ham review update ka feature bana rahe
        try:
           reviews=ReviewRating.objects.get(user__id=request.user.id,product__id=product_id)
           form=ReviewForm(request.POST,instance=reviews)
           form.save()
           messages.success(request,"Thank you ! your review has been updated")
           return redirect(url)
        except ReviewRating.DoesNotExist:
            form=ReviewForm(request.POST)
            if form.is_valid():
                data=ReviewRating()
                data.subject=form.cleaned_data['subject']
                data.rating=form.cleaned_data['rating']
                data.review=form.cleaned_data['review']
                data.ip=request.META.get('REMOTE_ADDR')
                data.product_id=product_id
                data.user_id=request.user.id
                data.save()
                messages.success(request,"Thank You !your review has been submitted")
                return redirect(url)

