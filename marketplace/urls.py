from django.urls import path
from marketplace import views

urlpatterns = [
    path("marketpl/",views.MarketPlace,name='marketpl'),
    path("restaurantmenu/<int:pk>/",views.RestaurantMenu,name="restaurantmenu"),
    path("addtocart/<int:pk>/<int:rest_id>/",views.add_to_cart,name="addtocart"),
    path("removefromcart/<int:pk>/<int:rest_id>/",views.remove_from_cart,name="removefromcart"),
    path("cart/",views.Cart_view,name="cart"),

]