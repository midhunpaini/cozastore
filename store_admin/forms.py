from django import forms
from django.forms import ModelForm
from store.models import CategoryOffer, Coupon, ProductOffer

class CouponOfferForm(ModelForm):
    class Meta:
        model = Coupon
        fields =( "name","coupon_code", "is_expired","discount","minimum_amount","validity", "discount_type")
       
        widgets = {
            'name':  forms.TextInput( attrs={ 'class':"form-control", 'id':"coupon_name", 'placeholder':'Name', 'style':'background-color:white; color:black'}),
            'coupon_code':  forms.TextInput( attrs={ 'class':"form-control", 'id':"coupon_code", 'placeholder':'Coupon Code', 'style':'background-color:white; color:black'}),
            'is_expired':  forms.CheckboxInput( attrs={ 'class':"form-control", 'id':"coupon_status",'value':'1'}),
            'discount':  forms.TextInput( attrs={ 'class':"form-control", 'id':"coupon_discount", 'placeholder':'Discount amount', 'style':'background-color:white; color:black'}),
            'minimum_amount':  forms.TextInput( attrs={ 'class':"form-control", 'id':"coupon_minimum_amount", 'placeholder':'Minimum Value Required', 'style':'background-color:white; color:black'}), 
            'validity':  forms.DateInput( attrs={ 'type':'date','class':"form-control", 'id':"coupon_validity",  'style':'background-color:white; color:black'}), 
            'discount_type':  forms.Select( attrs={ 'class':"form-control custom-select", 'id':"coupon_discount_type", 'style':'background-color:white; color:black'}),
        }
        
        
class CategoryOfferForm(ModelForm):
    class Meta:
        model = CategoryOffer
        fields =( "category","discount","minimum_amount","validity","discount_type")
    
        widgets = {
            'category':  forms.Select( attrs={ 'class':"form-control custom-select", 'id':"category_name", 'style':'background-color:white; color:black'}),
            'discount':  forms.TextInput( attrs={ 'class':"form-control", 'id':"category_discount", 'placeholder':'Discount amount', 'style':'background-color:white; color:black'}),
            'minimum_amount':  forms.TextInput( attrs={ 'class':"form-control", 'id':"category_minimum_amount", 'placeholder':'Minimum Value Required', 'style':'background-color:white; color:black'}),  
            'validity':  forms.DateInput( attrs={ 'type':'date','class':"form-control", 'id':"category_validity",  'style':'background-color:white; color:black'}),
            'discount_type':  forms.Select( attrs={ 'class':"form-control custom-select", 'id':"category_discount_type", 'style':'background-color:white; color:black'}),
        }
        
        
class ProductOfferForm(ModelForm):
    class Meta:
        model = ProductOffer
        fields =( "product","discount","minimum_amount","validity","discount_type")
        
        widgets = {
            'product':  forms.Select( attrs={ 'class':"form-control custom-select", 'id':"product_name", 'style':'background-color:white; color:black'}),
            'discount':  forms.TextInput( attrs={ 'class':"form-control", 'id':"product_discount", 'placeholder':'Discount amount', 'style':'background-color:white; color:black'}),
            'minimum_amount':  forms.TextInput( attrs={ 'class':"form-control", 'id':"product_minimum_amount", 'placeholder':'Minimum Value Required', 'style':'background-color:white; color:black'}),  
            'validity':  forms.DateInput( attrs={ 'type':'date','class':"form-control", 'id':"product_validity",  'style':'background-color:white; color:black'}),
            'discount_type':  forms.Select( attrs={ 'class':"form-control custom-select", 'id':"product_discount_type", 'style':'background-color:white; color:black'}),
        }
        
        

