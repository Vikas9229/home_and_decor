from django.urls import path
from .import views


urlpatterns = [
    path('store/',views.store,name="store"),
    path('category/<slug:category_slug>/',views.store,name="product_by_category"),
    path('category/<slug:category_slug>/<slug:product_slug>/',views.product_detail,name="product_detail"),
    path('search/',views.search,name="search"),
    path('submit_review/<int:product_id>/',views.submit_review,name="submit_review"),
    path("architects/", views.architects, name='architects'),
    path("architects_upload/", views.architect_upload,name='architect_upload'),
    path("architects_profile/", views.architect_profile,name='architect_profile'),
    path("contact/", views.contact,name='contact')
]