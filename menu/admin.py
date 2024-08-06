from django.contrib import admin
from menu.models import Category,FoodItem

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}


class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('food_name',)}


admin.site.register(Category,CategoryAdmin)
admin.site.register(FoodItem,FoodItemAdmin)

