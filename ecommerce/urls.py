"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('store/',include('store.urls')),
    path('carts/',include('carts.urls')),
    path('accounts/',include('accounts.urls')),
    path('orders/',include('orders.urls')),
    path("decor_idea/", views.decor_idea, name='decor_idea'),
    path("home_solution/", views.home_solution, name='home_solution'),
    path("interior_designers/",views.interior_designers, name='interior_designers'),
    path("events/", views.events, name='events'),
    path("vastu_shastra/", views.vastu_shastra, name='vastu_shastra'),
    # content urls
    path("img8_content/", views.img8_content, name='img8_content'),
    path("img1_content/", views.img1_content, name='img1_content'),
    path("img10_content/", views.img10_content, name='img10_content'),
    path("img3_content/", views.img3_content, name='img3_content'),
    path("imgdecor_content/", views.imgdecor_content, name='imgdecor_content'),
    path("img11_content/", views.img11_content, name='img11_content'),
    path("img12_content/", views.img12_content, name='img12_content'),
    path("img13_content/", views.img13_content, name='img13_content'),
    path("new1_content/", views.new1_content, name='new1_content'),
    # interior designer
    path("img15_content/", views.img15_content, name='img15_content'),
    path("img16_content/", views.img16_content, name='img16_content'),
    path("img17_content/", views.img17_content, name='img17_content'),
    path("img18_content/", views.img18_content, name='img18_content'),
    path("img19_content/", views.img19_content, name='img19_content'),
    path("img20_content/", views.img20_content, name='img20_content'),
    path("img21_content/", views.img21_content, name='img21_content'),
    path("img22_content/", views.img22_content, name='img22_content'),
    path("img23_content/", views.img23_content, name='img23_content'),
    path("img24_content/", views.img24_content, name='img24_content'),

    path("img26_content/", views.img26_content, name='img26_content'),
    path("img27_content/", views.img27_content, name='img27_content'),
    path("img28_content/", views.img28_content, name='img28_content'),

    path("img29_content/", views.img29_content, name='img29_content'),
    path("img30_content/", views.img30_content, name='img30_content'),
    path("img31_content/", views.img31_content, name='img31_content'),
    path("img32_content/", views.img32_content, name='img32_content'),
    path("img33_content/", views.img33_content, name='img33_content'),
    path("img34_content/", views.img34_content, name='img34_content'),
    path("img35_content/", views.img35_content, name='img35_content'),
    path("img36_content/", views.img36_content, name='img36_content'),
    path("img37_content/", views.img37_content, name='img37_content'),
    path("img38_content/", views.img38_content, name='img38_content'),
    path("img39_content/", views.img39_content, name='img39_content'),
    path("img40_content/", views.img40_content, name='img40_content'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


