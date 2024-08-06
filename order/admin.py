from django.contrib import admin
from order.models import Payment,Order,OrderedFood


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number','created_at','first_name','order_placed_to','status')
    list_filter = ('status',) 



# Register your models here.
admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderedFood)

