
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.views import View  # Corrected import of View
from django.http import JsonResponse
import razorpay
from django.conf import settings
from .models import Cart, OrderPayment, OrderPlaced, Product, Wishlist
from .forms import CustomerProfileForm, CustomerRegistrationForm, Customer
from . import views
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Customer
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views






def home(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/home.html', locals())

def about(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/about.html", locals())

def contact(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, "app/contact.html", locals())



class CategoryView(View):  # Inherit from View, not view
    def get(self, request,val=None):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())
        

class CategoryTitle(View):
    def get(self,request,val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product  = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())

class ProductDetail(View):
    def get(self, request, pk):
        totalitem = 0
        wishitem = 0
        wishlist = False  # ✅ Define default value for non-authenticated users

        product = get_object_or_404(Product, pk=pk)

        if request.user.is_authenticated:
            totalitem = Cart.objects.filter(user=request.user).count()
            wishitem = Wishlist.objects.filter(user=request.user).count()
            wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()

        return render(request, "app/productdetail.html", {
            'product': product,
            'totalitem': totalitem,
            'wishitem': wishitem,
            'wishlist': wishlist
        })
    
class CustomerRegistrationView(View):
    def get(self, request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        # Check if the user is already authenticated
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', locals())
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User Registered Successfully")
            #return redirect('login')  # Ensure 'login' is a valid URL name in urls.py
        else:
            messages.warning(request, "Invalid Input Data.")
        return render(request, "app/customerregistration.html", locals())

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/profile.html', locals())
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user , name=name ,locality=locality ,city=city, mobile=mobile ,state=state ,zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulations! Profile Save Successfully")
        else:
            messages.warning(request, "Invalid Input Data.")
        return render(request, 'app/profile.html', locals())
 
 
@login_required
def address(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add})

@method_decorator(login_required, name='dispatch')
class UpdateAddress(View):
    def get(self, request,pk):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        # Check if the user is already authenticated
        form = CustomerProfileForm()
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html', locals())

    def post(self, request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            totalitem = 0
            wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Congratulations! Address Updated Successfully")
        else:
            messages.warning(request, "Invalid Input Data.")
        return redirect('address')
@login_required
def add_to_cart(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')
@login_required
def show_cart(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
        totalamount = amount + 40
    return render(request, 'app/addtocart.html',locals())

@login_required
def show_wishlist(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    user = request.user
    product = Wishlist.objects.filter(user=user)
    return render(request, 'app/wishlist.html', locals())

@method_decorator(login_required, name='dispatch')
class checkout(View):
    def get(self, request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {'amount': razoramount, 'currency': 'INR', 'receipt': 'order_rcptid_12'}
        payment_response = client.order.create(data=data)
        print(payment_response)
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = razorpay.Payment(user=user, 
            amount=totalamount, 
            telebir_order_id=order_id, 
            telebir_payment_status=order_status)
            payment.save()
            messages.success(request, "Order Created Successfully")


        return render(request, 'app/checkout.html', locals())

# class checkout(View):  # Class name should start with uppercase C
#     def get(self, request):
#         totalitem = 0
#         wishitem = 0
#         if request.user.is_authenticated:
#             totalitem = len(Cart.objects.filter(user=request.user))
#             wishitem = len(Wishlist.objects.filter(user=request.user))
        
#         user = request.user
#         add = Customer.objects.filter(user=user)
#         cart_items = Cart.objects.filter(user=user)
#         famount = 0
#         for p in cart_items:
#             value = p.quantity * p.product.discounted_price
#             famount += value
        
#         totalamount = famount + 40
#         order_id = f"test_order_{user.id}"
#         order_status = "created"

#         # Save payment using the custom table/model
#         payment = OrderPayment.objects.create(
#             user=user,
#             amount=totalamount,
#             telebir_order_id=order_id,
#             telebir_payment_status=order_status
#         )

#         messages.success(request, "Test order created successfully")

#         return render(request, 'app/orderpayment.html', locals())
@login_required
def payment_done(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')
    user = request.user
    customer = Customer.objects.get(id=cust_id)
    razorpay.Payment.paid = True
    razorpay.Payment.telebir_payment_id = payment_id
    razorpay.Payment.save()
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity, payment=razorpay.Payment).save()
        c.delete()
    return redirect('/orders')

@login_required
def orders(request):
    totalitem = 0
    wishitem = 0    
    order_placed = OrderPlaced.objects.filter(user=request.user)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.filter(user=request.user).annotate(total_price=Count('product__discounted_price') * Count('quantity'))
    return render(request, 'app/orders.html', locals())

@login_required
def plus_cart(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    if request.method == 'GET':
        prod_id= request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={ 
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)
    

@login_required
def minus_cart(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    if request.method == 'GET':
        prod_id= request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={ 
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


@login_required
def remove_cart(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    if request.method == 'GET':
        prod_id= request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={ 
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)
    

@login_required
def plus_wishlist(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    # Check if the user is already authenticated
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(id=prod_id)
        user = request.user

        # Avoid adding duplicates
        if not Wishlist.objects.filter(user=user, product=product).exists():
            Wishlist.objects.create(user=user, product=product)

        return JsonResponse({'message': "Added to wishlist"})


@login_required
def minus_wishlist(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    # Check if the user is already authenticated
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(id=prod_id)
        user = request.user

        Wishlist.objects.filter(user=user, product=product).delete()
        return JsonResponse({'message': "Removed from wishlist"})
def search(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    query = request.GET.get('search')
    product = Product.objects.filter(Q(title__icontains=query) | Q(category__icontains=query))
    return render(request, 'app/search.html', locals())