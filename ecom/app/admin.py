from email.headerregistry import Group
from django.contrib import admin
from . models import Cart, OrderPlaced, Payment, Product, Wishlist
from .models import Customer 
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.models import Group

# Register your models here.
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id' , 'title' , 'discounted_price' , 'category' , 'product_image']
    def product_image(self, obj):
        if obj.product_image:
            return format_html('<img src="{}" style="width: 100px; height: 100px;" />', obj.product_image.url)
        return None

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id' , 'user' , 'locality' , 'city' , 'state', 'zipcode']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id' , 'user' , 'products' , 'quantity']
    def products(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id' , 'user' , 'amount' , 'telebir_order_id' ,'telebir_payment_status',
     'telebir_payment_id' , 'paid']
     
    

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id' , 'user' , 'customer','products' , 'quantity' , 'ordered_date' , 'status','payment']
    def products(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)

@admin.register(Wishlist)
class WhishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id' , 'user' , 'products']
    def products(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)
    
admin.site.unregister(Group)