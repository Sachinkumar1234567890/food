from accounts.models import User,UserProfile
from marketplace.models import * 

def get_vendor(request):
    try:
        vendor = User.objects.get(user=request.user)
        profile = UserProfile.objects.get(user=request.user) 
        u=User.objects.get(user=request.user)
    except:
        vendor = None
        profile = None
        u=None
    return dict(vendor = vendor, profile = profile,u=u)

# def count_cart_item(request):
#     cart_count=0
#     if request.user.is_authenticated:
#         try:
#             cart_item = Cart.objects.all()
#             for item in cart_item:
#                 cart_count += item.quantity
#         except:
#             cart_count = 0
#     return dict(cart_count=cart_count)

# @login_required(login_url='user_login')

def count_cart_item(request):
        cart_items = Cart.objects.all()
        cart_count=0
        if request.user.is_authenticated:
            for item in cart_items:
                if request.user.email == item.user.email:
                    try:
                        cart_count += item.quantity
                    except:
                        cart_count = 0
                else:
                     pass
        return dict(cart_count=cart_count)  