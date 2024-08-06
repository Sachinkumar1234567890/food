from django.shortcuts import render,redirect
from menu.models import Category,FoodItem
from vendor.models import Vendor
from menu.forms import AddCategoryForm,AddFoodItemForm,EditCategory_form,EditFoodItemForm
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify


# Create your views here.
def get_vendor(request):
    vendor=Vendor.objects.get(user=request.user)
    print(vendor)
    return vendor

def MenuBuilder(request):
    vendor = Vendor.objects.get(user=request.user)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    return render(request,'menu/MenuBuilder.html',{'categories':categories})

def FoodItem_By_Category(request,pk=None):
    vendor = Vendor.objects.get(user=request.user)
    category = get_object_or_404(Category,id=pk)
    var = FoodItem.objects.filter(vendor=vendor, category=category)
    return render(request,'menu/FoodItem_By_Category.html',{'var':var})

def AddCategory(request):
    form = AddCategoryForm()
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor= get_vendor(request)
            category.slug= slugify(category_name)
            form.save()
            return redirect('menu')
    return render(request,'menu/AddCategory.html',{'form':form})


def AddFoodItem(request):
    form = AddFoodItemForm()
    if request.method == 'POST':
        form = AddFoodItemForm(request.POST,request.FILES)
        if form.is_valid():
            food_name = form.cleaned_data['food_name']
            food = form.save(commit=False)
            food.vendor= get_vendor(request)
            food.slug= slugify(food_name)
            form.save()
            return redirect('menu')
    return render(request,'menu/AddFoodItem.html',{'form':form})


def deleteFoodCategory(request,pk):
    data = Category.objects.get(id=pk)
    print(data)
    data.delete()
    return redirect('menu')

def EditFoodCategory(request,pk):
    res = Category.objects.get(id=pk)
    print(res)
    if request.method == 'POST':
        form = EditCategory_form(request.POST,instance=res)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor= get_vendor(request)
            category.slug= slugify(category_name)
            form.save()
            return redirect('menu')

    form = EditCategory_form(instance=res)
    return render(request,'menu/EditCategory.html',{'form':form})


def deleteFoodItem(request,pk):
    data = FoodItem.objects.get(id=pk)
    data.delete()
    return redirect('menu')


def EditFoodItem(request,pk):
    res = FoodItem.objects.get(id=pk)
    print(res)
    if request.method == 'POST':
        form = EditFoodItemForm(request.POST,request.FILES,instance=res)
        if form.is_valid():
            food_name = form.cleaned_data['food_name']
            food = form.save(commit=False)
            food.vendor= get_vendor(request)
            food.slug= slugify(food_name)
            form.save()
            return redirect('menu')

    form = EditFoodItemForm(instance=res)
    return render(request,'menu/EditFoodItem.html',{'form':form})






