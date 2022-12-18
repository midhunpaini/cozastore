
import datetime
from datetime import datetime, timedelta
from time import strftime
from django.shortcuts import render,redirect
from store.models import *
from django.contrib.auth import authenticate,login,logout
from store.models import *
from django.http import JsonResponse,HttpResponse
from django.conf import settings
import csv
from store.templatetags.cart import *
import calendar
# Create your views here.


def dashboard(request):
    orders= Order.objects.all()
    cod = Order.objects.filter(payment_method='cod').count()
    paypal = Order.objects.filter(payment_method='paypal').count()
    razorpay = Order.objects.filter(payment_method='razorpay').count()
    returned = Order.objects.filter(order_status='return').count()
    pending = Order.objects.filter(order_status='pending').count()
    delivered = Order.objects.filter(order_status='delivered').count()
    canceled = Order.objects.filter(order_status='canceled').count()
    products_today = Order.objects.filter(order_date__gte=datetime.now().date())
    
    m = []
    for month in range(12):
        m.append(Order.objects.filter(order_date__month = month+1, payment_status='success').count()) 
    print(m[11],'asdfasdf') 
 

    sales_today = 0
    for product in products_today:
        price = int(product.items.product.price)
        quantity = int(product.items.quantity)
        t_price = price*quantity
        sales_today+=t_price
     
    
    total_sales = 0
    for product in orders:
        price = int(product.items.product.price)
        quantity = int(product.items.quantity)
        t_price = price*quantity
        total_sales+=t_price
    
    total_proft = 0
    no_of_items = 0
    for product in orders:
        price = int(product.items.product.price)-int(product.items.product.cost)
        quantity = int(product.items.quantity)
        profit = price*quantity
        total_proft+=profit
        no_of_items+=quantity
    
    
    profit_today = 0
    no_of_items = 0
    for product in products_today:
        price = int(product.items.product.price)-int(product.items.product.cost)
        quantity = int(product.items.quantity)
        profit = price*quantity
        profit_today+=profit
        no_of_items+=quantity
        
        
        
        

    context = {
        'orders':orders,
        'cod':cod,
        'paypal':paypal,
        'razorpay':razorpay,
        'returned': returned,
        'pending': pending,
        'delivered': delivered,
        'canceled': canceled,
        'sales_today':sales_today,
        'total_sales': total_sales,
        'total_profit':total_proft,
        'profit_today':profit_today,
        'jan': m[0],
        'feb': m[1],
        'mar' : m[2],
        'april':m[3],
        'may':m[4],
        'june':m[5],
        'july':m[6],
        'aug':m[7],
        'sept':m[8],
        'oct':m[9],
        'nov':m[10],
        'dec':m[11],
    }

    return render(request, 'store_admin/index.html',context)


def get_data(request):
    data ={
        'sales':100,
        'customers':10
    }
    return JsonResponse(data)

def admin_signin(request):
    if request.method != 'POST':
        return render(request,'store_admin/login.html')
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username = username, password = password)
    if user is None:
        return render(request, 'store_admin/login.html', {'error': 'Bad Credentials'})

    login(request, user)

    return redirect('dashboard')

def signout(request):
    logout(request)
    print('logout')
    return redirect('admin_signin')

def products(request):
    products = Products.objects.all()
    context = {'products':products}
    return render(request, 'store_admin/products.html', context)


def accounts(request):
    # sourcery skip: assign-if-exp, boolean-if-exp-identity, remove-unnecessary-cast
  
    users = Customer.objects.all().order_by('id').values()
    if request.method == 'POST':
        id = request.POST.get('user_id')
        user = Customer.objects.get(id=id)
        if user.active == True:
            user.active = False
            
        else:
            user.active = True
        user.save()
        return render(request, 'store_admin/accounts.html',{'users':users})


    return render(request, 'store_admin/accounts.html',{'users':users})

def filters(request):
    categories = Category.objects.all()
    colors = Color.objects.all()
    size = Size.objects.all()
    tags = Tags.objects.all()
    filters = {
        'categories': categories,
        'colors': colors,
        'size': size,
        'tags': tags
    }
    if request.method == 'POST':
       
            category = request.POST.get('category')
            size = request.POST.get('size')
            color = request.POST.get('color')
            tag = request.POST.get('tag')
            
            if size != None:
                new_size = Size.objects.create(value=size)
                new_size.save()
            
            if color != None:
                new_color = Color.objects.create(value=color)
                new_color.save()
            
            if tag != None:
                new_tag = Tags.objects.create(name=tag)
                new_tag.save()
            
            if category != None:
                new_category = Category.objects.create(name=category)
                new_category.save()
       
            return render(request, 'store_admin/category.html')

    return render(request, 'store_admin/category.html',{'filters':filters})

def edit_filters(request):
    categories = Category.objects.all()
    colors = Color.objects.all()
    size = Size.objects.all()
    tags = Tags.objects.all()
    filters = {
        'categories': categories,
        'colors': colors,
        'size': size,
        'tags': tags
    }   
    return render(request, 'store_admin/edit-category2.html',{'filters':filters})

def edit_category(request):
    if request.method=='POST':
        id = request.POST.get('edit')
        if id != None:
            category = Category.objects.get(id=id)
            name = request.POST.get('name')
            category.name = name
            category.save()
            return redirect('edit_filters')
        else:
            try:
                id = request.POST.get('delete')
                category = Category.objects.get(id=id)
                category.delete()
            except Exception:
                pass
    return redirect('edit_filters')

def edit_color(request):
    if request.method=='POST':
        id = request.POST.get('edit')
        if id != None:
            color = Color.objects.get(id=id)
            value = request.POST.get('value')
            color.value = value
            color.save()
            return redirect('edit_filters')
        else:
            try:
                id = request.POST.get('delete')
                color = Color.objects.get(id=id)
                color.delete()
            except Exception:
                pass
    return redirect('edit_filters')

def edit_size(request):
    if request.method=='POST':
        id = request.POST.get('edit')
        if id != None:
            size = Size.objects.get(id=id)
            value = request.POST.get('value')
            size.value = value
            size.save()
            return redirect('edit_filters')
        else:
            try:
                id = request.POST.get('delete')
                size = Size.objects.get(id=id)
                size.delete()
            except Exception:
                pass
    return redirect('edit_filters')

def order_manage(request):
    all_orders = Order.objects.all().order_by('-order_date')
    return render(request, 'store_admin/order.html', {'all_orders':all_orders})

def cancel_order_admin(request):
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
    
def confirm_order_admin(request):
    if request.method == 'GET':
        order_id = request.GET['order_id']
        order = Order.objects.get(id=order_id)
        order.order_status = 'accepted'
        order.save()
        order_item_id = order.items.id
        order_item = OrderCart.objects.get(id=order_item_id) 
        order_item.customer_order_status = 'accepted'
        order_item.save()
        return JsonResponse({'sucess':True}) 
    
def ship_order_admin(request):
    if request.method == 'GET':
        order_id = request.GET['order_id']
        order = Order.objects.get(id=order_id)
        order.order_status = 'shipped'
        order.save()
        order_item_id = order.items.id
        order_item = OrderCart.objects.get(id=order_item_id) 
        order_item.customer_order_status = 'shipped'
        order_item.save()
        return JsonResponse({'sucess':True}) 
    

def deliver_order_admin(request):
    if request.method == 'GET':
        order_id = request.GET['order_id']
        order = Order.objects.get(id=order_id)
        order.order_status = 'delivered'
        order.delivery_date = datetime.now().today()
        order.payment_status = 'success'
        order.save()
        order_item_id = order.items.id
        order_item = OrderCart.objects.get(id=order_item_id) 
        order_item.customer_order_status = 'delivered'
        order_item.save()
        return JsonResponse({'sucess':True}) 
    
    
def refund_order(request):
    if request.method == 'GET':
        order_id = request.GET['order_id']
        order = Order.objects.get(id=order_id)
        if order.payment_status == 'success':
            order.payment_status = 'refunded'
        order.save()
        order_item_id = order.items.id
        order_item = OrderCart.objects.get(id=order_item_id) 
        if order.payment_status == 'success':
            order_item.customer_order_status = 'refunded'
        else:
            order_item.customer_order_status = 'returned'
        order_item.save()
    return JsonResponse({'sucess':True}) 
    
def customer_order(request,oid):
        if 'user_id' in request.session:
            order = Order.objects.get(id=oid) 
            ordercart = order.items
            print(ordercart,'sdfasdfasdfasdfas')
            print(oid,'customer.id') 
            context ={
                'order_id':oid,
                'ordercart':ordercart
                }    
            return render(request, 'store_admin/customer_order.html',context)

def report(request):
    from_date = datetime.now().date()
    to_date = datetime.now().date() + timedelta(days=1)
    orders = Order.objects.filter(payment_status='success').order_by('-order_date')
    context = {
        'orderss':orders,
        'daily':'daily',
        'from':from_date,
        'to':to_date
    } 
    return render(request, 'store_admin/report.html',context)
   

def daily_report(request):
    orders = Order.objects.filter(order_date__gte=datetime.now().date(),payment_status='success').order_by('-order_date')
    from_date = datetime.now().date()
    to_date = datetime.now().date() + timedelta(days=1)
    print(from_date,'sdafasdfa')
    context = {
        'orderss':orders,
        'daily':'daily',
        'from':from_date,
        'to':to_date
    }
        
    return render(request, 'store_admin/report.html',context)


def monthly_report(request,month):
    orders = Order.objects.filter(order_date__month = month, payment_status='success').order_by('-order_date')
    from_date = '01'+month+'2022'
    to_date = '30'+month+'2022'
    context = {
        'orderss':orders,
        'from':from_date,
        'to':to_date
        
    }
        
    return render(request, 'store_admin/report.html',context)

def yearly_report(request):
    last_year = datetime.now().date() - timedelta(days=365)
    to_date = datetime.now().date()
    orders = Order.objects.filter(order_date__lte=datetime.now().date(),order_date__gte=last_year,payment_status='success').order_by('-order_date')
    context = {
        'orderss':orders,
        'yearly':'yearly',
        'from':last_year,
        'to':to_date
    }
    return render(request, 'store_admin/report.html',context)


def filter_report(request,from_date,to_date):
    print(from_date)
    orders = Order.objects.filter(order_date__lte=to_date,order_date__gte=from_date,payment_status='success').order_by('-order_date')
    return render(request, 'store_admin/report.html',{'orderss':orders})


from store.helpers import html2pdf  
def download_report(request,from_date,to_date):
    orders = Order.objects.filter(order_date__lte=to_date,order_date__gte=from_date,payment_status='success').order_by('-order_date')
    
    total_proft = 0
    no_of_items = 0
    for product in orders:
        price = int(product.order_price)-int(product.items.product.cost)
        quantity = int(product.items.quantity)
        profit = price*quantity
        total_proft+=profit
        no_of_items+=quantity
        
    context ={
        'orderss':orders,
        'profit':total_proft,
        'no_of_items':no_of_items
    }
    print('you are at report download')   
    pdf=html2pdf('store_admin/report_download.html',context)
    return HttpResponse(pdf,content_type='application/pdf')

def download_report_csv(request,from_date,to_date):
    print('inside csv')
    response = HttpResponse(content_type = 'text/csv')
    response['content-Disposition'] = 'attachment; filename = report.csv'
    
    writer = csv.writer(response)
    
    orders = Order.objects.filter(order_date__lte=to_date,order_date__gte=from_date,payment_status='success').order_by('-order_date')
    
    total_proft = 0
    no_of_items = 0
    for product in orders:
        price = int(product.order_price)-int(product.items.product.cost)
        quantity = int(product.items.quantity)
        profit = price*quantity
        total_proft+=profit
        no_of_items+=quantity
        print(total_proft)
        
    writer.writerow(['SALES REPORT FOR',from_date,' TO ',to_date])
    writer.writerow(['PRODUCT NAME', 'USER','COST PRICE', 'DISCOUNT', 'SELLING PRICE', 'QUANTITY',
                     'PAYMENT METHOD', 'PROFIT'])
    for order in orders:
        writer.writerow([order.items.product.name,order.items.product.cost,
                         order.order_price-order.items.product.price,
                         order.order_price, no_of_items,  order.payment_method,
                         order.order_price-order.items.product.cost])
    writer.writerow(['TOTAL PROFIT = ','' ,'' ,'' ,total_proft])

    return response

from store_admin import forms
def offer(request):
    coupon_form = forms.CouponOfferForm()
    category_form = forms.CategoryOfferForm()
    product_form = forms.ProductOfferForm()
    coupon_offers = Coupon.objects.all()
    category_offers = CategoryOffer.objects.all()
    product_offers = ProductOffer.objects.all()
    
    context = {
        'form':coupon_form,
        'category_form':category_form,
        'product_form':product_form,
        'coupon_offers':coupon_offers,
        'category_offers':category_offers,
        'product_offers':product_offers
    }
    return render(request,'store_admin/offers.html',context)

def set_coupon(request):
    if request.method == 'POST':
        coupon_name = request.POST.get('coupon_name')
        coupon_code = request.POST.get('coupon_code')
        discount = request.POST.get('discount')
        discount_type = request.POST.get('discount_type')
        minimum_amount = request.POST.get('minimum_amount')
        validity = request.POST.get('coupon_validity')
           
        Coupon.objects.create(name=coupon_name, discount= discount, coupon_code=coupon_code, discount_type=discount_type, validity=validity, minimum_amount=minimum_amount)
        
        return JsonResponse({'success':True})
    


def set_category_offer(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_name')
        discount = request.POST.get('category_discount')
        discount_type = request.POST.get('discount_type')
        minimum_amount = request.POST.get('minimum_amount')
        validity = request.POST.get('category_validity')
        
        category = Category.objects.get(id=category_id)
        
        CategoryOffer.objects.create(category=category, discount_type=discount_type, discount=discount, validity=validity, minimum_amount=minimum_amount)
        
        return JsonResponse({'success':True})
    
    

def set_product_offer(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_name')
        discount = request.POST.get('product_discount')
        discount_type = request.POST.get('discount_type')
        
        validity = request.POST.get('product_validity')
        product = Products.objects.get(id=product_id)
        minimum_amount = product.price
        ProductOffer.objects.create(product=product, discount_type=discount_type, discount=discount, validity=validity, minimum_amount=minimum_amount)
        
        return JsonResponse({'success':True})
    
def cancel_offer(request):
    if request.method == 'POST':
        print('canceloffer ***************************')
        offer_type = request.POST.get('offer_type')
        offer_id = request.POST.get('offer_id')
        if offer_type == 'product':
            offer = ProductOffer.objects.get(id = offer_id)
            offer.is_expired = True
            offer.save()
        elif offer_type == 'coupon':
            offer = Coupon.objects.get(id = offer_id)
            offer.is_expired = True
            offer.save()
        else:
            offer = CategoryOffer.objects.get(id = offer_id)
            offer.is_expired = True
            offer.save()
        return JsonResponse({'success':True})