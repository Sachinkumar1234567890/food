from django.shortcuts import render
from order.forms import OrderForm
from django.shortcuts import render,redirect, HttpResponse
from vendor.models import Vendor
from marketplace.models import Cart
from accounts.models import User,UserProfile
from menu.models import Category,FoodItem
from django.http import HttpResponse,HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from order.models import Order,OrderedFood
from order.utils import get_order_number
import razorpay
from ecommerce.settings import RAZORPAY_KEY_ID,RAZORPAY_SECRET_KEY
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from marketplace.models import Cart


razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_SECRET_KEY))

def AddOrder(request):
    cart_items = Cart.objects.filter(user=request.user)
    counts = cart_items.count
    food_items = FoodItem.objects.filter(id__in=[item.fooditem_id for item in cart_items])
    print(food_items)
    total_amount = 0    
    for item in cart_items:
        food_item = food_items.get(id=item.fooditem_id)
        total_amount += item.quantity * food_item.price
    
    delivery_charge = 0
    if total_amount < 500:
        delivery_charge = 20
    elif total_amount < 1000:
        delivery_charge = 10

    
    total_amount += delivery_charge

    sgst = round(total_amount * 0.06 ,2)
    cgst = round(total_amount * 0.06 ,2) 
    
    total_amount_with_gst = total_amount + sgst + cgst
    total_amount_with_gst_rounded = round(total_amount_with_gst, 2)

   # Billing address 

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

    # orders = Order.objects.filter(user=request.user).first()
    orders, created = Order.objects.get_or_create(user=request.user, defaults={'total': total_amount_with_gst_rounded, 'total_tax': cgst + sgst})
    print(orders,'hdddddddddddddddddddddddddd')

    for carts in cart_items:
        obj = OrderedFood(
                order=orders,
                user=request.user,
                fooditem=carts.fooditem,
                quantity=carts.quantity,
                price=carts.fooditem.price,
                amount=total_amount_with_gst_rounded
            )
        obj.save()

    address=Order.objects.all()
    for i in address:
        i.email == request.user.email
        add=i

        print(request.user.email)
    
    print(orders)
    # form = OrderForm(initial=default_values)
    razorpay_order_id = None
    currency = 'INR'
    amount = None
    name = None
    if request.method == 'POST':
        print("hi")
        form = OrderForm(request.POST, initial=default_values)
        form.save()
        print(form)
        
    #     if form.is_valid():
    print("hello")
    #orders = form.save(commit=False)
    orders.user = request.user
    orders.total = total_amount_with_gst_rounded
    orders.total_tax = cgst + sgst
    orders.payment_method = 'razorpay'
    orders.first_name = request.user.first_name
    orders.last_name = request.user.last_name
    orders.phone = request.user.phone_number
    #         form.save()
    orders.order_number = get_order_number(orders.id)
    orders.is_ordered = True
    orders.status=orders.STATUS[2][0]
    print(orders.status)
    orders.save()
    
    currency = 'INR'
    amount =  int((orders.total) * 100)
    name=orders.first_name +' '+ orders.last_name
    print(amount) 
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,currency=currency,payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler'
    redirect("order_complete")

    print(razorpay_order_id)
    print(callback_url)
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = RAZORPAY_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url

    if orders.status == 'Completed':
        obj = Cart.objects.all().delete()
      
            
            
            
    context={
        "counts": counts,
        'cart_items': cart_items,
        'food_items': food_items,
        'total_amount': total_amount_with_gst_rounded,
        'sgst': sgst,
        'cgst': cgst,
        'delivery_charge': delivery_charge,
        'rzp_order_id': razorpay_order_id,
        'RAZOR_KEY_ID':RAZORPAY_KEY_ID,
        'form': form,
        'amount':amount,
        'name':name,
        'address':address,
        'add':add,
        #'orders':orders       
    }
                
    return render(request, 'order/proceed_to_order.html',context)




@csrf_exempt
def paymenthandler(request):
    print("Payment")
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            # signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                # 'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = amount  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return render(request, 'order/paymentsuccess.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'order/paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'order/paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
    
def ordercomplete(request):
    order = Order.objects.filter(user=request.user).latest('created_at')
    ordered_items = OrderedFood.objects.filter(order=order)
    print(ordered_items)
    total_amount = sum(item.amount for item in ordered_items)
    print(total_amount) 

    delivery_charges = 0
    if total_amount < 500:
        delivery_charges = 20
    elif total_amount < 1000:
        delivery_charges = 10
   


    print(delivery_charges)
    total_amount += delivery_charges

    sgst = round(total_amount * 0.06 ,2)
    cgst = round(total_amount * 0.06 ,2) 
    total_amount+=sgst+cgst
    print(total_amount)
    

    order_number = order.order_number
    order_username = order.user.username
    order_date = order.created_at
    order_status = order.status
    is_ordered = order.is_ordered

    context = {
        'order':order,
        'order_number': order_number,
        'order_username': order_username,
        'order_date': order_date,
        'order_status': order_status,
        'is_ordered': is_ordered,
        'ordered_items': ordered_items,
        'total_amount': total_amount,
        'cgst': cgst,
        'sgst': sgst,
        'delivery_charges': delivery_charges,
    }

    return render(request, 'order/order_complete.html', context)

def Restaurant_Orders(request):
    # orders=Order.objects.all()


    # vendor = Vendor.objects.get(user=request.user)
    # orders = Order.objects.filter(vendor__in=[vendor.id], is_ordered=True).order_by('created_at')
    # recent_orders = orders[:10]

    context = {
        # 'orders': orders,
        # 'orders_count': orders.count(),
        # 'recent_orders': recent_orders
    }

    return render(request, 'order/Restaurant_Orders.html', context)



