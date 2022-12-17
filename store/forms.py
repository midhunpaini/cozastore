from django import forms
from django.forms import ModelForm
from . models import ShippingAddress

class AddressForm(ModelForm):
    class Meta:
        model = ShippingAddress
        fields =("fname", "lname", "phone", "email", "pincode", "state", "address1", "address2")
        
        widgets = {
            'fname':  forms.TextInput( attrs={ 'class':"form-control", 'id':"add_fname", 'placeholder':'First Name'}),
            'lname':  forms.TextInput( attrs={ 'class':"form-control", 'id':"add_lname", 'placeholder':'Last Name'}),
            'email':  forms.EmailInput( attrs={ 'class':"form-control", 'id':"add_email", 'placeholder':'Email Address'}),
            'phone':  forms.TextInput( attrs={ 'class':"form-control", 'id':"add_mobile", 'placeholder':'Mobile'}),
            'pincode':  forms.TextInput( attrs={ 'class':"form-control", 'id':"add_pin", 'placeholder':'Pincode'}),
            'state':  forms.TextInput( attrs={ 'class':"form-control", 'id':"add_state", 'placeholder':'State'}),
            'address1':  forms.TextInput( attrs={ 'class':"form-control", 'id':"add_address1", 'placeholder':'Address'}),
            'address2':  forms.TextInput( attrs={ 'class':"form-control", 'id':"add_address2", 'placeholder':'Address'}), 
        }
        
        



class EditCustomerPassword(forms.Form):
    current_password = forms.CharField(label='Current Password' , widget=forms.PasswordInput(attrs={ 'class':"form-control", 'id':"current_password"}))
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={ 'class':"form-control", 'id':"new_password"}))
    conf_new_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={ 'class':"form-control", 'id':"edit_confirm_password"}))