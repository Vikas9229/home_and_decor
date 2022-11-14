from django.urls import path
from .import views

urlpatterns = [
    path('register/',views.register,name="register"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('forgotPassword/',views.forgotPassword,name="forgotPassword"),
    path('resetPassword/',views.resetPassword,name="resetPassword"),
    path('activate/<uidb64>/<token>/',views.activate,name="activate"),
    path('reset_password_validate/<uidb64>/<token>/',views.reset_password_validate,name="reset_password_validate"),
    path('',views.dashboard,name="dashboard"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('my_orders/',views.my_orders,name='my_orders'),
    path('change_password/',views.change_password,name='change_password'),

]