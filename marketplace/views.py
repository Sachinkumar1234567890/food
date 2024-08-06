from django.shortcuts import render,get_object_or_404,redirect

from vendor.models import Vendor
from accounts.models import UserProfile,User
from menu.models import Category,FoodItem
from django.db.models import Prefetch
from marketplace.models import Cart
from django.http import HttpResponse
from order.models import *
from order.forms import *



# Create your views here.

def MarketPlace(request):
    if 'S' in request.GET:
        S = request.GET['S']
        print(S)
        ven_data = Vendor.objects.filter(restaurant_name__icontains=S,is_approved=True,user__is_active=True)
    else:
        ven_data = Vendor.objects.filter(is_approved=True, user__is_active=True)
    ven_profile=UserProfile.objects.all()
    count = ven_data.count()
    return render(request, 'marketplace/MarketPlacePage.html', {'count': count, 'ven_data': ven_data, 'ven_profile':ven_profile})


    # # ven_data1 = Vendor.objects.filter()
    # ven_data = Vendor.objects.filter(is_approved=True,user__is_active=True)
    # print(ven_data)
    # # ven_profile = User.objects.filter(is_active=True)
    # # print(ven_profile) 
    # # count= ven_data1.count()
    # count=ven_data.count()
    # ven_profile=UserProfile.objects.all()
    # return render(request,'marketplace/MarketPlacePage.html',{'ven_data':ven_data,'count':count,'ven_profile':ven_profile})


def RestaurantMenu(request,pk):
    cart=Cart.objects.all()
    vendor = get_object_or_404(Vendor,pk=pk)
    rest_id=pk
    print(rest_id)
    category = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',FoodItem.objects.filter(is_available=True)
        )
    )
    ven_profile=UserProfile.objects.get(user=vendor.user)
    return render(request,'marketplace/RestaurantMenu.html',{'category':category,'vendor':vendor,'ven_profile':ven_profile,'rest_id':rest_id,'cart':cart})


def add_to_cart(request,pk,rest_id):
    if request.user.is_authenticated:
        try:
            food_item=FoodItem.objects.get(id=pk)
            price=food_item.price
            try:
                check_cart= Cart.objects.get(user=request.user,fooditem=food_item)
                check_cart.quantity+=1
                check_cart.total= check_cart.quantity*check_cart.fooditem.price
                check_cart.save()
                return redirect("restaurantmenu",rest_id)
                
            except:
                check_cart= Cart.objects.create(user=request.user,fooditem=food_item,quantity=1,total=price)
                return redirect("restaurantmenu",rest_id)

        except:
            return redirect("restaurantmenu",rest_id)

    else:
        return redirect("user_login")
        
   
def remove_from_cart(request,pk,rest_id):
    if request.user.is_authenticated:
            try:
                food_item=FoodItem.objects.get(id=pk)
                check_cart= Cart.objects.get(user=request.user,fooditem=food_item)
                if check_cart.quantity > 1:
                    check_cart.quantity-=1
                    check_cart.total= check_cart.quantity*check_cart.fooditem.price
                    check_cart.save()
                else:
                    check_cart.delete()
                return redirect("restaurantmenu",rest_id)

            except:
                return redirect("restaurantmenu",rest_id)

    else:
        return redirect("user_login")


def Cart_view(request):
    user_details = UserProfile.objects.get(user=request.user)
    default_values={
        'first_name':request.user.first_name,
        'last_name':request.user.last_name,
        'email':request.user.email,
        'phone':request.user.phone_number,
        'address':user_details.address,
        'city':user_details.city,
        'state':user_details.state,
        'pin_code':user_details.pincode,
    }
    form = OrderForm(initial=default_values)
    price = 0
    delivery_fee = 0
    grand_total = 0
    cart_items = Cart.objects.filter(user=request.user)
    print(cart_items)
    # for i in cart_items:
    #         print("yesssssssssssssssssssssssssss ")
    #     else:
    #         print("nooooooooooooooooooooooooooo")

    for i in cart_items:
        if request.user.email == i.user.email:
            price += i.quantity*i.fooditem.price
            if price>0 and price<250:
                delivery_fee=50
            elif price>=250 and price<500:
                delivery_fee=30
            elif price>=500:
                delivery_fee= 0
            else:
                delivery_fee=0

            gst=price*0.06
            gst=gst.__round__(2)
            grand_total = price+gst*2+delivery_fee
            grand_total=grand_total.__round__(2)
        else:
            pass

    if request.method == 'POST':
        selected_option = request.POST.get("pay")
        if selected_option == "paypal":
            return HttpResponse("Page under maintannance")
        elif selected_option == "razorpay":
            return redirect("proceed")
        
    email = request.user.email

    return render(request,'marketplace/Cart.html',{'cart_items':cart_items,'gst':gst,'delivery_fee':delivery_fee,'grand_total':grand_total,'form':form,'email':email})



    



