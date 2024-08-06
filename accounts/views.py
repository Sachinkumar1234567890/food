from django.shortcuts import render,redirect
from accounts.forms import *
from vendor.forms import *
from accounts.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.utils import detectUser,send_verification_email
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator 
from vendor.models import Vendor
from order.models import Order


# Create your views here.

# ristict vendor to go user dashbrd
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied
    

def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied



@login_required(login_url='user_login')
def index(request):
    return render(request,'index.html',{})


def UserRegistration(request):
    if request.user.is_authenticated:
        messages.warning(request,"you have already logged in")
        return redirect("Myaccount")
    elif request.method == "POST":
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user=User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password) 
            user.set_password(password)
            user.role=user.CUSTOMER
            user.save()

            # Send verification email
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request,"Hey thanks for Register...!")
            return redirect('user_login')
        else:
            print("error occured")
            print(form.errors)
    else:
        form=UserRegistrationForm()
    return render(request,'accounts/userRegister.html',{'form':form})

def VendorRegistration(request):
    if request.user.is_authenticated:
        messages.warning(request,"you have already loged in")
        return redirect("Myaccount")
    if request.method == "POST":
        form=UserRegistrationForm(request.POST)
        form_v=VendorRegistrationForm(request.POST,request.FILES)
        if form.is_valid() and form_v.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user=User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password) 
            user.role=user.VENDOR
            user.save() 
            vendor=form_v.save(commit = False)
            vendor.user = user
            vendor.save()

            # Send verification email
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            user_profile = UserProfile.objects.get(user=user)
            print(user_profile)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request,"Your restaurant details registered successfully, Please wait for admin approval..!")
    else:
        form=UserRegistrationForm()
        form_v=VendorRegistrationForm()

    return render(request,'vendorRegister.html',{'form':form,'form_v':form_v})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,"Congratulations! Your account is activated")
        return redirect('Myaccount')  
    else:
        messages.success(request,"Invalid activation link")
        return redirect('Myaccount')    


def user_login(request):
    message ="hello"
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        user=authenticate(email=email,password=password)
        if user:
            if user.is_active:
                login(request,user)
                messages.success(request,"Login successful")
                return redirect("Myaccount")
            else:
                messages.warning(request,"User is not active")
                return redirect("user_login")
        else:
            messages.warning(request,"Pls check your credentials")
            return redirect("user_login")
    return render(request,"login.html",{'message':message})

@login_required(login_url='user_login')
def user_logout(request):
    logout(request)
    return redirect('user_login')

@login_required(login_url='user_login')
def Myaccount(request):
    user=request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='user_login')
@user_passes_test(check_role_customer)
def userdashboard(request):


    return render(request,"userdashboard.html",{})

@login_required(login_url='user_login')
@user_passes_test(check_role_vendor)
def vendordashboard(request):
    # orders=Order.objects.all()
    vendor = Vendor.objects.get(user=request.user)
    orders = Order.objects.filter(vendor__in=[vendor.id], is_ordered=True).order_by('created_at')
    recent_orders = orders[:10]

    # //////////////////////////////////////////////////////////
    # vendor=Vendor.objects.get(user=request.user)
    profile= UserProfile.objects.get(user=request.user)
    print("Vendor",vendor)
    print("Orders",orders)

    context = {
        'orders': orders,
        'orders_count': orders.count(),
        # 'recent_orders': recent_orders
        # ////////////////////////////////////////////////////
        'vendor':vendor,
        'profile':profile
    }
     
    return render(request,"vendordashboard.html",context)






