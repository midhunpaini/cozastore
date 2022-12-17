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
        
        
        def clean(self):
 
            super(AddressForm, self).clean()
            fname = self.cleaned_data.get('fname')
            phone = self.cleaned_data.get('phone')
            email = self.cleaned_data.get('email')
            pincode = self.cleaned_data.get('pincode')
            state = self.cleaned_data.get('state')
            address1 = self.cleaned_data.get('address1')
     
            if len() < 4:
                self._errors['fname'] = self.error_class([
                    'Minimum 4 characters required'])
            if len() !=10:
                self._errors['phone'] = self.error_class([
                    'Enter a valid mobile number'])
            if len() < 12 :
                self._errors['email'] = self.error_class([
                    'Enter a valid Email address'])
                
            if len() != 6 :
                self._errors['email'] = self.error_class([
                    'Enter a valid Pincode'])
            if len() < 3 :
                self._errors['state'] = self.error_class([
                    'Enter a valid State'])
            if len() < 7 :
                self._errors['address1'] = self.error_class([
                    'Minimum 15 characters required'])
    
            return self.cleaned_data



class EditCustomerPassword(forms.Form):
    current_password = forms.CharField(label='Current Password' , widget=forms.PasswordInput(attrs={ 'class':"form-control", 'id':"current_password"}))
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={ 'class':"form-control", 'id':"new_password"}))
    conf_new_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={ 'class':"form-control", 'id':"edit_confirm_password"}))