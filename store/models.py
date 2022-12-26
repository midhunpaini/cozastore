import pytz
from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import User
from django.core import validators



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True, validators=[validators.validate_email])
    mobile = models.CharField(max_length=13,null=True)
    password = models.CharField(max_length=200, null=True)
    active = models.BooleanField(default=True)
    

    
    def __str__(self):
        return self.name
    @property
    def wishlist(self):
        wish = self.wishlist_set.all()
        return wish


class Size(models.Model):
    size_choice = {
        ('XL','XL'), ('L','L'),('M','M'),('S','S')
    }
    value = models.CharField(max_length=100,choices=size_choice,default='M', null=True)
    
    def __str__(self):
        return self.value

 
    
class Color(models.Model):
    value = models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return self.value
 
 
 
    
class Tags(models.Model):
    name = models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return self.name   
    
 
   
class Category(models.Model):
    name = models.CharField(max_length=50, null=True)
    subcategory = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    
    
class Products(models.Model):
    name = models.CharField(max_length=200, null=True)
    image = models.ImageField(null=True, blank = True)
    description = models.CharField(max_length=250, null=True, blank=True)  
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, blank = True, null = True)
    tags = models.ForeignKey(Tags, on_delete = models.SET_NULL, blank = True, null = True)
    price = models.FloatField()
    cost = models.FloatField( null=True, blank=True)
    stock = models.IntegerField()
    date_entry = models.DateTimeField(auto_now_add = True )
    image = models.ImageField(null=True, blank=True, upload_to='')
    image2 = models.ImageField(null=True, blank=True, upload_to='')
    image3 = models.ImageField(null=True, blank=True, upload_to='')
    
    def __str__(self):
        return self.name
    
    @staticmethod
    def get_all_product():
        return Products.objects.all()
    
    @staticmethod
    def get_all_product_by_id(category_id):
        if category_id:
            return Products.objects.filter(category = category_id)
        else:
            return Products.get_all_product()
      
    
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except Exception:
            url = ''
        return url
    


class ProductVariation(models.Model):
    product = models.ForeignKey(Products, on_delete = models.CASCADE, blank = True, null = True) 
    color = models.ForeignKey(Color, on_delete = models.CASCADE, blank = True, null = True)   
    size = models.ForeignKey(Size, on_delete = models.CASCADE, blank = True, null = True) 
    
    @staticmethod   
    def get_all_product_by_color(color_id):
        if color_id:
            return ProductVariation.objects.filter(color = color_id)
        else:
            return Products.get_all_product()
        
    @staticmethod   
    def get_all_product_by_size(size_id):
        if size_id:
            return ProductVariation.objects.filter(size = size_id)
        else:
            return Products.get_all_product()
     
class Coupon(models.Model):
    offer_choice = {
        ('FLAT','FLAT'), ('PERCENTAGE','PERCENTAGE')
    }
    name = models.CharField(max_length=100, null=True, blank=True)
    coupon_code = models.CharField(max_length=50)
    is_expired = models.BooleanField(default=False)
    discount = models.IntegerField()
    discount_type = models.CharField(max_length=100,choices=offer_choice,default='FLAT', null=True, blank=True)
    minimum_amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    validity = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name  
    




class CategoryOffer(models.Model):
    
    offer_choice = {
        ('FLAT','FLAT'), ('PERCENTAGE','PERCENTAGE')
    }
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, blank = True, null = True)
    is_expired = models.BooleanField(default=False)
    discount = models.IntegerField()
    minimum_amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    validity = models.DateField(null=True, blank=True)
    discount_type = models.CharField(max_length=100,choices=offer_choice,default='FLAT', null=True, blank=True)
    
    # def __str__(self):
    #     return self.category.name  
    

class ProductOffer(models.Model):
    
    offer_choice = {
        ('FLAT','FLAT'), ('PERCENTAGE','PERCENTAGE')
    }
    product = models.ForeignKey(Products, on_delete = models.SET_NULL, blank = True, null = True)
    is_expired = models.BooleanField(default=False)
    discount = models.IntegerField()
    minimum_amount = models.IntegerField(null=True,blank=True)
    date = models.DateField(auto_now_add=True)
    validity = models.DateField(null=True, blank=True)
    discount_type = models.CharField(max_length=100,choices=offer_choice,default='FLAT', null=True, blank=True)
        
        

class Offer(models.Model):
    coupon_offer = models.ForeignKey(Coupon, on_delete = models.SET_NULL, blank = True, null = True)
    category_offer = models.ForeignKey(CategoryOffer, on_delete = models.SET_NULL, blank = True, null = True)
    product_offer = models.ForeignKey(ProductOffer, on_delete = models.SET_NULL, blank = True, null = True)
    

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, blank = True, null = True) 
    product = models.ForeignKey(Products, on_delete = models.SET_NULL, blank = True, null = True)
    quantity = models.IntegerField(default = 0, null = True, blank = True)
    
    def __str__(self):
        return str(self.id)
    


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, blank = True, null = True) 
    fname = models.CharField(max_length=20, null=False, blank=False)
    lname =models.CharField(max_length=20, null=True)
    phone =models.CharField(max_length=10, null=False, blank=False)
    email =models.EmailField(max_length=30, null=False, blank=False)
    pincode = models.CharField(max_length=6, null=False, blank=False)
    state = models.CharField(max_length=20, null=False, blank=False)
    address1 = models.CharField(max_length=150, null=False, blank=False)
    address2 = models.CharField(max_length=150, null=True)
    date = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.fname   
 

      
class OrderCart(models.Model):
    status_choices={
        ('pending','pending'),('accepted','accepted'),('canceled','canceled'),('return','return'),('shipped','shipped'),('delivered','delivered'),('refunded','refunded')
    }
    customer = models.CharField(max_length=100, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete = models.SET_NULL, blank = True, null = True)
    quantity = models.IntegerField(default = 0, null = True, blank = True)  
    customer_order_status = models.CharField(max_length=200, choices=status_choices, default='pending')
    coupon = models.ForeignKey(Coupon, on_delete= models.SET_NULL, blank=True, null=True)
    cart_date = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.product.name  
  
  
class Order(models.Model):
    status_choices={
        ('pending','pending'),('accepted','accepted'),('canceled','canceled'),('return','return'),('shipped','shipped'),('delivered','delivered')
    }
    p_status={
        ('success','success'),('failed','failed'),('pending','pending'),('refunded','refunded')
    }
    
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, blank = True, null = True)
    guest_user= models.CharField(max_length=200, null=True, blank=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete = models.CASCADE, blank = True, null = True)
    items = models.ForeignKey(OrderCart, on_delete = models.CASCADE, blank = True, null = True)  
    order_price = models.IntegerField(blank=True, null=True)
    discount_type = models.CharField(max_length=100, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add = True)
    delivery_date = models.DateTimeField(null=True,blank=True)
    payment_method = models.CharField(max_length=200, null=True)
    order_status = models.CharField(max_length=200, choices=status_choices, default='pending')
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=100, null=True, blank=True)
    paypal_id =  models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.CharField(max_length=200, choices=p_status, default='pending')
    return_reason = models.CharField(max_length=200, null=True, blank=True)
    return_order = models.BooleanField(default=False)
    
    
    def __str__(self):
        return str(self.id)
    @property
    def returnOrder(self):
        utc=pytz.UTC
        today = utc.localize(datetime.now())
        return_date = self.delivery_date + timedelta(days=7)
        if today<return_date:
            self.return_order = True
        return self.return_order

            
 
 
    
class UserAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, blank = True, null = True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete = models.CASCADE, blank = True, null = True)
    
    def __str__(self):
        return self.customer.name
    
class Wishlist(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, blank = True, null = True)
    product = models.ForeignKey(Products, on_delete = models.SET_NULL, blank = True, null = True)
    wish_date = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.product.name
    


    