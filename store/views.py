from django.shortcuts import render,redirect
from . models import *
from django.http import JsonResponse, HttpResponse,HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
import random
import json
from . twilio import MessageHandler
from . templatetags.cart  import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from io import BytesIO
from django .template.loader import get_template
import xhtml2pdf.pisa as pisa
import uuid
from django.conf import settings
import razorpay
import pytz
from . forms import *



def user_logged(request):
    return 'user_id' in request.session
    

def user_cart(request):
    return 'cart' in request.session


def customer(request):
    user_id = request.session.get('user_id')
    return Customer.objects.get(id = user_id)



def home(request):
    sizes = Size.objects.all()
    colors= Color.objects.all()
    
    products = None
    
    color_id =  request.GET.get('colorid')
    size_id =  request.GET.get('sizeid')
    price_range = request.GET.get('price_range')
    filter_p = request.GET.get('filter')
    all_product = request.GET.get('all_product')
 
    if color_id :
        products = Products.get_all_product_by_color(color_id)
    elif all_product:
        products = Products.objects.all()
    elif size_id:
        products = Products.get_all_product_by_size(size_id)
    elif price_range:
        price_range = int(price_range)
        products = Products.objects.filter(price__gte=price_range, price__lte=price_range+250)
    elif filter_p:
        if filter_p == 'new':
            products = Products.objects.all().order_by('-date_entry')  
        elif filter_p == 'low':
            products = Products.objects.all().order_by('price') 
        else:
            products = Products.objects.all().order_by('-price')       
    else:    
        products = Products.objects.all()[:4]
    
    context={
        'colors':colors,
        'products':products,
        'sizes':sizes
    }
    return render(request, 'store/home.html', context)


from django.db.models import Q
def search(request):
    if search_key := request.GET.get('search'):
        products = Products.objects.filter(Q(name__icontains = search_key))

    else:
        products = Products.objects.all()
    return render(request, 'store/product.html', {'products':products})


def about(request):
    products = Products.objects.all()
    return render(request, 'store/about.html',{'products':products})


def blog(request):
    products = Products.objects.all()
    return render(request, 'store/blog.html',{'products':products})


def contact(request):
    products = Products.objects.all()
    return render(request, 'store/contact.html',{'products':products})


def signup(request):
    
    if request.method == "POST":
        name = request.POST.get('uname')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        password = request.POST.get('password')
        conf_password=request.POST.get('conf_pass')    

        error_message = None
        
        if Customer.objects.filter(email=email).exists():
            error_message = "Email already registered!"
            return JsonResponse({'sucess':True,'error_message':error_message})

        elif name in ["", ' ', '   ']:
            error_message = "Please enter a valid name" 
            return JsonResponse({'sucess':True,'error_message':error_message})          

        elif Customer.objects.filter(mobile=mobile).exists():
            error_message=  "Mobie Number Already Registered!"
            return JsonResponse({'sucess':True,'error_message':error_message})


        elif password in ["", ' ', '   ']:
            error_message =  "Enter a valid password"
            return JsonResponse({'sucess':True,'error_message':error_message})

        elif password != conf_password:
            error_message = "Password not matching"  
            return JsonResponse({'sucess':True,'error_message':error_message})                            

        if not error_message:
            password = make_password(password)
            user=Customer.objects.create(name=name,email=email,mobile=mobile,password=password,)        
            user.save()
      
            return JsonResponse({'sucess':True})
        else:
            
            return render(request,'store/signin.html',)

    return render(request, 'store/signin.html')
    

def signin(request):
    
    if request.method != 'POST':
        return render(request, 'store/signin.html')
    email = request.POST['email']
    password = request.POST['password']

    message = None
    try:
        user = Customer.objects.get(email=email)

        if user.active== False:
            message = "You are blocked!"
            return JsonResponse({'sucess':True,'message':message})

        if check_password(password, user.password):
            request.session['user_id']=user.id
            
            request.session['user_name']=user.name
            get_user_cart(request)
            return JsonResponse({'sucess':True,})

    except Exception:
        message =  "Email not registered!"
    else:
        message =  "Enter a valid password!"
        return JsonResponse({'sucess':True,'message':message})
    return render(request, 'store/signin.html')



def user_logout(request):

    user_cart(request)
    request.session.flush()
    return render(request, 'store/home.html')


def otp_login(request):
    user = None
    if request.method == "POST":
        try:  
            phone_no = request.POST['mobile']
            user = Customer.objects.filter(mobile = phone_no).exists()
            if user:
                otp = random.randint(1000, 9999)
                request.session['otp'] = otp
                request.session['mobile'] = phone_no
               
                mobile = '+91' + phone_no
                MessageHandler(mobile,otp).send_otp()
                return JsonResponse({'sucess':True})
            else:
                user = None
                message =  "Mobile not registered!"
                return JsonResponse({'sucess':True,'message':message})
                
        except:
            Exception
        return JsonResponse({'sucess':True,'message':message})
            
    

def verify_otp(request):
    if request.method=='POST':
        customer_otp = int(request.POST['otp']) 
        otp = request.session.get('otp')
        mobile = request.session.get('mobile')
        user = Customer.objects.get(mobile=mobile)
    
        if customer_otp ==otp:
            request.session['user_id']=user.id
            request.session['user_name']=user.name
            get_user_cart(request)
            return JsonResponse({'sucess':True})
        else:
            message = "Wrong OTP"
            return JsonResponse({'sucess':True,'message':message})
    return redirect('home')

        
def profile(request):
    edit_pass_form = EditCustomerPassword()
    address_form = AddressForm()
    errors = address_form.errors
    wishlist = []
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        user = Customer.objects.get(id = user_id)
        wishlist = Wishlist.objects.filter(customer=user)
 
   
    context ={
        'edit_pass_form':edit_pass_form,
        'address_form':address_form,
        'errors':errors,
        'wishlist':wishlist
    }
    return render(request, 'store/user-profile.html', context)


def edit_account(request):
    if request.method =="POST":
        name = request.POST["user_name"]
        email = request.POST['email']
        mobile = request.POST['mobile']
        password = request.POST['password']
        user_id = request.session.get('user_id')
        user=Customer.objects.get(id=user_id)
        error_message = None
        if user.mobile == mobile:
            user.mobile =None
            user.save()
        if user.email == email:
            user.email = None
            user.save() 


        if Customer.objects.filter(mobile=mobile).exists():
            error_message=  "Mobie Number Already Registered!"
            return JsonResponse({'sucess':True,'error_message':error_message}) 
        
        elif Customer.objects.filter(email=email).exists():
            error_message = "Email already registered!"

            return JsonResponse({'sucess':True,'error_message':error_message})  
        
        if not error_message and check_password(password, user.password):
            user.name = name
            user.email = email
            user.mobile = mobile        
            user.save()
  
            return JsonResponse({'sucess':True})
        else:
            error_message=  "Invalid password!"
            return JsonResponse({'sucess':True,'error_message':error_message}) 
    return JsonResponse({'sucess':True})

def edit_password(request):
    if request.method =="POST":
        password = request.POST["current_pass"]
        new_pass = request.POST['new_pass']
        conf_new_pass = request.POST['conf_pass']
        
        user_id = request.session.get('user_id')
        user=Customer.objects.get(id=user_id)
        if check_password(password, user.password):            
            if new_pass == conf_new_pass:
               new_pass = make_password(new_pass)
               user.password = new_pass
               user.save()
            else:
                error_message = 'Passwords Not matching'
                return JsonResponse({'sucess':True,'error_message':error_message}) 
        else:
            error_message = 'Enter valid Password'
            return JsonResponse({'sucess':True,'error_message':error_message}) 
    return JsonResponse({'sucess':True})


def del_customer_address(request):
    if request.method == 'GET':
        address_id = request.GET['address_id']

        dele=UserAddress.objects.get(id = address_id)
        dele.delete()
        return JsonResponse({'sucess':True})
    
def edit_customer_address(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        address_id = request.POST.get('address_id') 
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address1 = request.POST.get('address')
        address2 = request.POST.get('address2')
        pincode = request.POST.get('pin')
        state = request.POST.get('state')

        up_address=ShippingAddress.objects.get(id=address_id) 
        try:
            up_address.fname=fname
            up_address.lname=lname
            up_address.email=email
            up_address.phone=mobile
            up_address.address1=address1
            up_address.address2=address2
            up_address.state=state
            up_address.pincode=pincode
            up_address.save()
            return JsonResponse({'sucess':True})
        except:

       
            return HttpResponse('error')


        


def add_customer_address(request):
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
         
            user_id = request.session.get('user_id')
            user = Customer.objects.get(id=user_id)
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            email = request.POST.get('email')
            mobile = request.POST.get('phone')
            address1 = request.POST.get('address1')
            address2 = request.POST.get('address2')
            pincode = request.POST.get('pincode')
            state = request.POST.get('state')
            shipping_address=ShippingAddress.objects.create(customer=user,fname=fname, lname=lname, email=email,phone=mobile,address1=address1,address2=address2,state=state, pincode=pincode)
            UserAddress.objects.create(customer=user, shipping_address=shipping_address)
            return render(request, 'store/user-profile.html',{'address_form':address_form})
        else:
  
            address_form = AddressForm()
          
            return render(request, 'store/user-profile.html',{'address_form':address_form})
        
        
def user_cart(request):
    if 'cart' not in request.session:
        return
    if "user_id" in request.session:
        customer_id = request.session.get('user_id')
        user = Customer.objects.get(id=customer_id)
        cart = request.session['cart']
        ids = list(cart.keys())
        values = list(cart.values())
        l = len(cart) 
        for x in range(l):
            id = int(ids[x])
            qty = int(values[x])
            product = Products.objects.get(id=id)
            if  Cart.objects.filter(customer=user,product=product).exists():
                c = Cart.objects.get(customer=user,product=product)
                c.quantity = qty
                c.save()
            else: 
                Cart.objects.update_or_create(product=product, customer=user, quantity=qty)
            
        
        
    
def get_user_cart(request):
    if 'user_id' in request.session:
        customer_id = request.session.get('user_id')
        user = Customer.objects.get(id=customer_id)
        c= Cart.objects.filter(customer=user)
        l = len(c)        
        for x in range(l):
            id = str(c[x].product.id)
            qty = c[x].quantity
            cart = request.session.get('cart')
            if cart:
                cart[id] = qty
            else:
                cart = {id: qty}

            request.session['cart'] = cart
            

           


def product(request):
    sizes = Size.objects.all()
    colors= Color.objects.all()

   
    products = None
    
    color_id =  request.GET.get('colorid')
    size_id =  request.GET.get('sizeid')
    price_range = request.GET.get('price_range')
    filter_p = request.GET.get('filter')
    all_product = request.GET.get('all_product')
    category = request.GET.get('cat')
    
    if color_id :
        products = Products.get_all_product_by_color(color_id)
    elif all_product:
        products = Products.objects.all()
    elif category:
        products = Products.objects.filter(category = category)
    elif size_id:
        products = Products.get_all_product_by_size(size_id)
    elif price_range:
        price_range = int(price_range)
        products = Products.objects.filter(price__gte=price_range, price__lte=price_range+250)
    elif filter_p:
        if filter_p == 'new':
            products = Products.objects.all().order_by('-date_entry')  
        elif filter_p == 'low':
            products = Products.objects.all().order_by('price') 
        else:
            products = Products.objects.all().order_by('-price')       
    else:    
        products = Products.get_all_product()
    
    context={
        'colors':colors,
        'products':products,
        'sizes':sizes,
      
    }   
    return render(request, 'store/product.html',context)


def delete_product(request):
    if request.method == 'POST':
        id = request.POST.get('delete_checkbox')
        try:
            product = Products.objects.get(id=id)
            product.delete()
        except:
            Products.DoesNotExist
        products = Products.objects.all()
        context = {'products':products}
 
    return render(request, 'store_admin/products.html', context)


def add_product(request):
    categorys = Category.objects.all()
    colors = Color.objects.all()
    sizes = Size.objects.all()
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            category = request.POST.get('category')
            category=Category.objects.get(name=category)
            color = request.POST.get('color')
            color = Color.objects.get(value=color)
            size = request.POST.get('size')
            size = Size.objects.get(value=size)
            description = request.POST.get('description')
            stock = request.POST.get('stock')
            price = request.POST.get('price')
            image = request.FILES.get('image')
            image2 = request.FILES.get('image2')
            image3 = request.FILES.get('image3')
            fprice = float(price)
            date = request.POST.get('entry_date')
        except Exception:
            
            color.DoesNotExist
            size.DoesNotExist
        
            
        new_product=Products.objects.create(
            name=name,
            color=color,
            category=category,
            size=size,
            description=description,
            stock=stock, 
            price = fprice,
            date_entry=date,
            image=image,
            image2 = image2,
            image3 = image3)
        new_product.save()
        return render(request, 'store_admin/add-product.html', {'categorys':categorys, 'colors':colors, 'sizes':sizes})

    return render(request, 'store_admin/add-product.html', {'categorys':categorys, 'colors':colors, 'sizes':sizes})


def get_product(request):  
    products = Products.objects.all()
    if request.method == 'POST':
        categorys = Category.objects.all()
        colors = Color.objects.all()
        size = Size.objects.all()
        id = request.POST.get('product_id')
        product = Products.objects.get(id=id)
        return render(request, 'store_admin/edit-product.html', {'product':product, 'categorys':categorys, 'colors':colors, 'size':size})           
    return render(request, 'store_admin/get-product.html', {'products':products})

def edit_product(request):
    if request.method == 'POST':
        id = request.POST.get('product_id')
        product = Products.objects.get(id=id)
        product.name = request.POST.get('name')
     
        product.description = request.POST.get('description')
        product.stock = request.POST.get('stock')
        price = request.POST.get('price')
        product.image = request.FILES.get('image')
        product.image2 = request.FILES.get('image2')
        product.image3 = request.FILES.get('image3')
        product.price = float(price)
        category = request.POST.get('category')
        color = request.POST.get('color')
        sizes = request.POST.get('size')
        category=Category.objects.get(name=category)
        color = Color.objects.get(value=color)
        size = Size.objects.get(value=sizes)
        product.category = category
        product.color = color
        product.size = size
        product.save()
        return redirect('get_product')
     
    # except Exception:
    #     category.DoesNotExist
    #     color.DoesNotExist
    #     size.DoesNotExist
    
    return redirect('edit_product')



# def modal(request):
#     if request.method == 'POST':
#         product_id = int(request.POST['product_id'])
 
#         mproduct = Products.objects.get(id=product_id)
#         cart = request.session.get('cart')
#         if cart:
#             cart_items = len(cart.values())
#         else:
#             cart_items = 0
#         data = {
#             'product_name': mproduct.name,
#             'product_description': mproduct.description,
#             'product_image': mproduct.imageURL,
#             'product_price': mproduct.price,
#             'product_color': str(mproduct.color),
#             'product_size': str(mproduct.size),
#             'product_id': product_id,
#             'cart_items': cart_items,
#         }
   
#         return JsonResponse({'success': True, 'data': data})
#     return render(request, 'store/modal.html')

def modal(request,id):
       
    product = Products.objects.get(id=id)
    data = {
        'product':product
        }
    return render(request, 'store/product-detail2.html',data)



def cart(request): 
    if request.method == 'GET':  
        if cart := request.session.get('cart'):
            keys = cart.keys()

            products_in_cart = []
            for id in keys:
                id = int(id)
                product = Products.objects.get(id=id)
                products_in_cart.append(product)
            data = {
            'products_in_cart':products_in_cart,
        }    
        else:
            data = {}     

    if request.method == 'POST': 
      
        product_id = request.POST['product_id']
        cart = request.session.get('cart')
        if cart:
            if product_id in cart.keys():
                cart[product_id] +=1
            else:
                cart[product_id] = 1
        else:
            cart = {product_id: 1}

        request.session['cart'] = cart
 
        keys = cart.keys()
        cart_count = len(keys)
        products_in_cart = []
        for id in keys:
            id = int(id)
            product = Products.objects.get(id=id)
            products_in_cart.append(product)
        cart_items = len(cart.values())
        data = {
            'products_in_cart':products_in_cart,
        }
        return JsonResponse({'cart_items':cart_items, 'cart_count':cart_count})
    try:
         return render(request,'store/shoping-cart.html',data)
    except:
        return render(request,'store/shoping-cart.html')


def modify_cart(request):
    if request.method != 'POST':
        return redirect('/')
    data = json.load(request)
    quantity = int(data.get('numProduct'))
    product_id = data.get('product_id')
    change = data.get('change')
    products = Products.objects.all()
    product = Products.objects.get(id = product_id)
    product_price = offer_price(product)
    carts = request.session.get('cart')
    
    
    new_quantity = quantity
   
    if change == 'plus' :
        new_quantity = quantity + 1
    elif quantity > 1:
        new_quantity = quantity - 1

    if new_quantity <= 10:
        total_price = product_price * new_quantity
    else:
        total_price = product_price * 10

    cart = request.session.get('cart')
    if cart:
        if quantity==10:
            cart[product_id] = 10
        elif change == 'plus' and quantity<10:
            cart[product_id] = quantity + 1
        elif change == 'minus' and quantity > 1:
            cart[product_id] = quantity - 1
    elif change == 'plus' and quantity < 10:
        cart = {product_id: quantity + 1}
    elif quantity > 1:
        cart = {product_id: quantity - 1}
    request.session['cart'] = cart

    
    discount_total = total_discount(products,carts)
    cart_price = total_cart_price(products, carts)
    sub_total = discount_total + cart_price
    

    datas = {
        'sucess':True,
        'total_price': total_price,
        'cart_price':cart_price,
        'new_quantity': new_quantity,
        'total_discount' :discount_total,
        'sub_total':sub_total
        
    }

    return JsonResponse(datas)

def check_cart(request):
    cart = request.session.get('cart')
 
    if cart == None:
        cart_items = 0
    else:
        cart_items = 1
    return JsonResponse({'sucess':True,'cart_items':cart_items})


def stock(request):
    product_id = request.GET['product_id']
    qty = request.GET['numProduct']

    product = Products.objects.get(id = product_id)
    product.stock>=qty
    return True

def del_cart_item(request):
    if request.method =='POST':
        data = json.load(request)
        product_id = data.get('product_id')
      
        if 'user_id' in request.session:
            
            user_id = request.session.get('user_id')
            user = Customer.objects.get(id = user_id)
            
            
            product = Products.objects.get(id = product_id)

            try:
                c = Cart.objects.get(customer= user, product= product)
                c.delete()
            except Exception:
                pass

        cart = request.session.get('cart')
        cart.pop(product_id)
        request.session['cart'] = cart
        
        products = Products.objects.all()
        cart_price = total_cart_price(products, cart)
        cart_items = len(cart.values())
   
        
        return JsonResponse({'success':True, 'cart_price':cart_price, 'cart_items':cart_items})
    return redirect('/')


def checkout(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        user_addresses = UserAddress.objects.filter(customer = user_id)
        
    if 'cart' not in request.session:
        return redirect('/')
    cart = request.session.get('cart')      
    keys = cart.keys()
    products_in_cart = []
    for id in keys:
        id = int(id)
        product = Products.objects.get(id=id)
        products_in_cart.append(product)        
    
    if request.method == 'POST':        
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('num-product1'))
        cart = request.session.get('cart')
        if cart:
            cart[product_id] = quantity
        else:
            cart = {product_id: quantity}

        request.session['cart'] = cart
        
        keys = cart.keys()
        products_in_cart = []
        for id in keys:
            id = int(id)
            product = Products.objects.get(id=id)
            products_in_cart.append(product)
        
        return render(request, 'store/checkout.html',{'cart_products':products_in_cart})
        
    return render(request, 'store/checkout.html',{'cart_products':products_in_cart})



def make_order(items,user_id,shipping_address,payment_option,discount,request,total_price):
    if user_logged(request):
        paypal_id = uuid.uuid4()
        razor_id = settings.RAZORPAY_ID
        razor_pass = settings.RAZORPAY_PASS
        client = razorpay.Client(auth=(razor_id, razor_pass))
        total_price-=discount
        payment = client.order.create({'amount':total_price*100, 'currency':'INR', 'payment_capture': 1})
        for item in items:
            item.product.stock -= item.quantity
            item.product.save()
            final_price = item.product.price-(discount/len(items))
            ordercart = OrderCart.objects.create(customer=user_id, product=item.product, quantity=item.quantity)
            
            if payment_option == 'cod':
                Order.objects.create(customer=customer(request),shipping_address=shipping_address, items=ordercart,payment_method =payment_option,order_price=final_price) 
                item.delete()
            
            elif payment_option == 'paypal':
                Order.objects.create(customer=customer(request),shipping_address=shipping_address, items=ordercart,payment_method =payment_option, paypal_id=paypal_id,order_price=final_price) 
                item.delete()
                return[paypal_id]
            
            else:
                Order.objects.create(customer=customer(request),shipping_address=shipping_address, items=ordercart,payment_method =payment_option,razorpay_payment_id= payment['id'],order_price=final_price) 
                item.delete()               
                return [payment,razor_id]
        




def order(request): 
    if request.method =='POST':

        cart = request.session.get('cart')
        products= Products.objects.all()
        total_price =total_cart_price_discount(products,cart)
        user_cart(request) 
        fname = request.POST['fname']
        coupon_code = request.POST['coupon_code']
        lname = request.POST['lname']
        phone = request.POST['phone']
        email = request.POST['email']
        pincode = request.POST['pincode']
        state = request.POST['state']
        address1 = request.POST['address1']
        address2 = request.POST['address2']
        save_address = request.POST['save_address']
        payment_option= request.POST['payment_option']
        address_option= request.POST['address_option']
        discount =  request.POST['discount']
        discount = float(discount)
        print(type(discount),'klasdjsdhflkashdfhasdhf')
        if user_logged(request):
            user_id = request.session.get('user_id')
            user = customer(request)
            items = Cart.objects.filter(customer=user)
    
 
        error_message = None
        if address_option == 'new':
            
            if len(fname) < 4 and fname in ["", ' ', '   ']:
                error_message = "Please enter a valid first name!"
                return JsonResponse({'error':True,'message':error_message})

            elif len(phone) !=10 and phone.isdigit():
                error_message = "Please enter a valid mobile number" 
                return JsonResponse({'error':True,'message':error_message})          


            elif len(pincode) !=6 and pincode.isdigit():
                error_message = "Please enter a valid mobile number" 
                return JsonResponse({'error':True,'message':error_message})   

            elif len(address1) < 4 and address1 in ["", ' ', '   ']:
                error_message = "Please enter a valid first name!"
                return JsonResponse({'error':True,'message':error_message}) 
            
            elif save_address =='true':
                shipping_address=ShippingAddress.objects.create(fname=fname,lname=lname,phone=phone,email=email,pincode=pincode,state=state,address1=address1,address2=address2)
                UserAddress.objects.create(customer = user, shipping_address=shipping_address)
            else:
                shipping_address=ShippingAddress.objects.create(fname=fname,lname=lname,phone=phone,email=email,pincode=pincode,state=state,address1=address1,address2=address2)
            
            

            if not error_message and payment_option == 'cod':
                print('iscount check', discount)
                make_order(items,user_id,shipping_address,payment_option,discount,request,total_price)
                del request.session['cart']
                return JsonResponse({'success':True,  'payment':payment_option}) 
            
    
            if not error_message and payment_option == 'paypal':
                paypal_id=make_order(items,user_id,shipping_address,payment_option,discount,request,total_price)
                cart_total = total_price - discount
                request.session['paypal_id'] = paypal_id
                del request.session['cart']
                return JsonResponse({'success':True, 'payment':payment_option, 'cart_total':cart_total,'paypal_id':paypal_id})
            
            if not error_message and payment_option == 'razorpay':
                order_values = make_order(items,user_id,shipping_address,payment_option,discount,request,total_price)
                del request.session['cart']
                return JsonResponse({'success':True, 'payment':payment_option, 'razorpay':order_values[0],'razor_id':order_values[1]})
            
        else:
            address_option = int(address_option)
            user_address = UserAddress.objects.get(id=address_option)
            shipping_address = user_address.shipping_address
            
            if not error_message and payment_option == 'cod':
                print('iscount check', discount)
                make_order(items,user_id,shipping_address,payment_option,discount,request,total_price)
                del request.session['cart']
                return JsonResponse({'success':True,  'payment':payment_option}) 
            
            if not error_message and payment_option == 'paypal':
                paypal_id = make_order(items,user_id,shipping_address,payment_option,discount,request,total_price)
                paypal_id = str(paypal_id)
                request.session['paypal_id'] = paypal_id
                cart_total = total_price - discount
                del request.session['cart']
                return JsonResponse({'success':True, 'payment':payment_option, 'cart_total':cart_total,'paypal_id':paypal_id})
            
            if not error_message and payment_option == 'razorpay':
                order_values = make_order(items,user_id,shipping_address,payment_option,discount,request,total_price)
                del request.session['cart']
                return JsonResponse({'success':True, 'payment':payment_option, 'razorpay':order_values[0],'razor_id':order_values[1]})


      
def paypal_success(request):
    if request.method =='GET':
        print('inside paypal')
        paypal_id = request.GET.get('paypal_id')
        print(paypal_id)
        orders = Order.objects.filter(paypal_id=paypal_id)
        for order in orders:
            print('inside lop paypal *******************************************')
            print(paypal_id, '     ',order.paypal_id)
            order.payment_status = 'success'
            print('payment success')
            order.save()
        del request.session['paypal_id']
    return JsonResponse({'success':True})



def razorpay_success(request):
    if request.method =='GET':
        order_search_id = request.GET['order_search_id'] 
        order_id = request.GET['razor_order_id'] 
        payment_id = request.GET['razor_payment_id']  
        razor_sign = request.GET['razor_sign']
        
        orders = Order.objects.filter(razorpay_payment_id=order_search_id)
        for order in orders:
            order.razorpay_order_id:order_id
            order.razorpay_payment_id = payment_id
            order.razorpay_signature = razor_sign
            order.payment_status = 'success'
            order.save()
        return JsonResponse({'success':True})

def razorpay_failed(request):
    if request.method =='GET':
        order_id = request.GET['order_search_id'] 
        orders = Order.objects.filter(razorpay_payment_id=order_id)
        for order in orders:
            order.payment_status = 'failed'
            order.order_status = 'canceled'
            order.items.product.stock += order.items.quantity 
            order.save()
    return JsonResponse({'success':True})

 
    
def cancel_order(request):
    if request.method == 'GET':
        order_id = request.GET['order_id']
        order_item_id = request.GET['order_item_id']
        order = Order.objects.get(id=order_id)
        order.order_status = 'canceled'
        order.save()
        order_item = OrderCart.objects.get(id=order_item_id) 
        order_item.customer_order_status = 'canceled'
        order_item.product.stock += order_item.quantity 
        order_item.save()
    
        return JsonResponse({'sucess':True})

def return_order(request):
    if request.method == 'GET':
        order_id = request.GET['order_id']
        order_item_id = request.GET['order_item_id']
        order = Order.objects.get(id=order_id)
        order.order_status = 'return'
        order.save()
        order_item = OrderCart.objects.get(id=order_item_id) 
        order_item.customer_order_status = 'return'
        order_item.product.stock += order_item.quantity 
        order.return_order = True
        order_item.save()
       
        return JsonResponse({'sucess':True})
    
def order_info(request):
    if request.method == 'GET':
        order_id = request.GET['order_id']
        order = Order.objects.get(id=order_id)
        product = order.items.product
        context = {
            'sucess':True,
            'product_name':product.name,
            'product_price' :product.price,
            'product_color':str(product.color),
            'product_size': str(product.size),
            'product_image':product.imageURL,
            'product_quantity':order.items.quantity           
            
        }
       
        return JsonResponse(context)                
       


from .helpers import html2pdf      
def create_invoice(request,id):
    order = Order.objects.get(id=id)
    total_price = int(order.items.product.price)*int(order.items.quantity)
    pdf=html2pdf('store/invoice.html',{'order':order, 'total_price':total_price})
    return HttpResponse(pdf,content_type='application/pdf')

def discounts(request):
    discount_type = request.GET.get('discount_type')
    return JsonResponse({})

def apply_coupon(request):
    if request.method == 'GET':
        coupon_code = request.GET['coupon_code']
        discount = 0
        other_discount = 0
        cart_value = 0
        coupons = Coupon.objects.all()
        for coupon in coupons:
            if coupon.is_expired == False:    
                if coupon_code == coupon.coupon_code:
                    discount = coupon.discount
                    cart_value = coupon.minimum_amount
                    break
            else:
                discount = -1
            
                
        context = {
           'success':True,
           'discount':discount,
           'cart_value':cart_value 
        }
  
    return JsonResponse(context)   


def wishlists(request):
    if request.method == "GET" and 'user_id' in request.session:
        product_id = request.GET.get('product_id')
        product = Products.objects.get(id=product_id)
        user_id = request.session.get('user_id')
        user = Customer.objects.get(id=user_id)
        wish_count = Wishlist.objects.filter(customer=user).count()
        x = is_in_wish(product,user_id)
       
        if not x :
            Wishlist.objects.create(customer=user,product=product)
            message = 1
        else:
            wish = Wishlist.objects.filter(customer=user,product=product)
            message = 0
            wish.delete()
        context = {
           'success':True,  
           'message':message,
           'wish_count':wish_count
        }
       
        return JsonResponse(context) 
    return JsonResponse({'success':True, 'message':2}) 


def remove_wishlists(request):
    if request.method == "GET":
        product_id = request.GET.get('product_id')
      
        product = Products.objects.get(id=product_id)
       
        user_id = request.session.get('user_id')
        user = Customer.objects.get(id=user_id)
        wish_count = Wishlist.objects.filter(customer=user).count()-1
        
        wish=Wishlist.objects.get(customer=user,product=product)
      
        wish.delete()
        message = 0
     
        context = {
           'success':True,  
           'message':message,
           'wish_count':wish_count,
        }

    return JsonResponse(context) 


    