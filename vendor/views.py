from django.shortcuts import render,redirect
from .forms import *
from order.forms import OrderForm
from vendor.forms import *


# Create your views here.

def Restaurentprofile(request):
    res = UserProfile.objects.get(user = request.user)
    
    res1= Vendor.objects.get(user = request.user)
    if request.method == 'POST':
        form = VendorProfile(instance=res)
        form1= VendorRegistrationForm(instance=res1)
        form = VendorProfile(request.POST,request.FILES,instance=res)
        form1=VendorRegistrationForm(request.POST,request.FILES,instance=res1)
        if form.is_valid():
            form.save()
            form1.save()        
            redirect("rprofile")
    form = VendorProfile(instance=res)
    form1 = VendorRegistrationForm(instance=res1)

    return render(request,'vendor/Rprofile.html',{'form':form,'form1':form1})


def Restaurant_Timings(request):

    vendor_data= Vendor.objects.get(user=request.user)
    TimeForm = OpeningHoursForm(request.POST,instance=vendor_data)

    print(vendor_data)
    if request.method == "POST":
        if TimeForm.is_valid():

            TimeForm.save()

        else:
            print('Else')
    timing_table = Opening_Hours.objects.all()

    return render(request,'vendor/Opening_hours.html',{'TimeForm':TimeForm,'timing_table':timing_table})

def DeleteTime(request,pk):
    time = Opening_Hours.objects.get(id=pk)
    time.delete()
    return redirect('timings')



