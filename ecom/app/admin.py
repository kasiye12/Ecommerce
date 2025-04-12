from django.contrib import admin
from . models import Cart, OrderPlaced, Payment, Product
from .models import Customer 

# Register your models here.
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id' , 'title' , 'discounted_price' , 'category' , 'product_image']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id' , 'user' , 'locality' , 'city' , 'state', 'zipcode']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id' , 'user' , 'product' , 'quantity']

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id' , 'user' , 'amount' , 'telebir_order_id' ,'telebir_payment_status',
     'telebir_payment_id' , 'paid']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id' , 'user' , 'customer','product' , 'quantity' , 'ordered_date' , 'status','payment']