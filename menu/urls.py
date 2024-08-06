from django.urls import path
from menu import views

urlpatterns = [
    path("menu/",views.MenuBuilder,name='menu'),
    path("fooditembycategory/category/<int:pk>",views.FoodItem_By_Category,name='fooditembycategory'),
    path("addcategory/",views.AddCategory,name='addcategory'),
    path("addfooditem/",views.AddFoodItem,name='addfooditem'),
    path("deletefoodcategory/<int:pk>/",views.deleteFoodCategory,name='deletefoodcategory'),
    path("editfoodcategory/<int:pk>/",views.EditFoodCategory,name='editfoodcategory'),
    path("deletefooditem/<int:pk>/",views.deleteFoodItem,name='deletefooditem'),
    path("editfooditem/<int:pk>/",views.EditFoodItem,name='editfooditem'),
    



]