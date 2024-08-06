from django import forms
from menu.models import Category,FoodItem

class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name','description']


class AddFoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['category','food_name','description','images','price','is_available']

class EditCategory_form(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name','description']


class EditFoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['category','food_name','description','images','price','is_available']


