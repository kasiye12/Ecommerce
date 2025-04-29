from django.db import models
from django.contrib.auth.models import User



STATE_CHOICES=(
    ('AA','Addis Ababa'),
    ('AF','Afar'),
    ('AM','Amhara'),
    ('BG','Benishangul-Gumuz'),
    ('DR','Dire Dawa'),
    ('GB','Gambela'),
    ('HR','Harari'),
    ('OR','Oromia'),
    ('SM','Somali'),
    ('SE','South Ethiopia'),
    ('SER','Southwest Ethiopia Peoples Region'),
    ('TR','Tigray'),
)
CATEGORY_CHOICES=(
    ('CR','Curd'),
    ('ML','Milk'),
    ('LS','Lassi'),
    ('MS','Milkshake'),
    ('PN','Panner'),
    ('GH','Ghee'),
    ('CZ','Cheese'),
    ('IC','Ice-Creams'),
)


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default="")
    prodapp = models.TextField(default="")
    #brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='products/', null=True, blank=True)
    def _str_(self):
        return self.title

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)  # Fixed typo
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15)
  
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=100)

    def __str__(self):  # Fixed method 2name
        return self.name
    
class supply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)  # Fixed typo
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15)
  
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=100)

    def __str__(self):  # Fixed method 2name
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
STATE_CHOICES=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the way','On the way'),
    ('Delivered','Delivered'),
    ('Cancelled','Cancelled'),
    ('Pending','Pending'),
)
    
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    telebir_order_id = models.CharField(max_length=100, blank=True, null=True)
    telebir_payment_status = models.CharField(max_length=100,blank=True, null=True)
    telebir_payment_id = models.CharField(max_length=100,blank=True, null=True)
    paid = models.BooleanField( default="False")
    def __str__(self):
        return str(self.user) + " - " + str(self.amount)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATE_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE, default="")
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
   
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)



class OrderPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    telebir_order_id = models.CharField(max_length=100)
    telebir_payment_status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"
