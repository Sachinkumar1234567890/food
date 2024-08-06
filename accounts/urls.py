from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("",views.index,name='index'),
    path("userregister/",views.UserRegistration,name='userregister'),
    path("vendorregister/",views.VendorRegistration,name='vendorregister'),
    path("user_login/",views.user_login,name='user_login'),
    path("userdashboard/",views.userdashboard,name='userdashboard'),
    path("vendordashboard/",views.vendordashboard,name='vendordashboard'),
    path("user_logout/",views.user_logout,name='user_logout'),
    path("Myaccount/",views.Myaccount,name='Myaccount'),
    path("activate/<uidb64>/<token>",views.activate ,name="activate"),
    
   

  path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "reset_password.html"), name ='reset_password'),
  path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "password_reset_sent.html"), name ='password_reset_done'),
  path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "password_reset_form.html"), name ='password_reset_confirm'),
  path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "password_reset_done.html"), name ='password_reset_complete')



]