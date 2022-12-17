from . models import *
from datetime import datetime,timedelta

def customer_name(request):
    if 'user_id' in request.session:
        customer_name = request.session.get('user_name')
        return {'customer_name':customer_name}
    else:
        return{}

def shipping_address(request):
    if 'user_id' not in request.session:
        return{}
    user_id = request.session.get('user_id')
    user = Customer.objects.get(id = user_id)
    print(user.wishlist)
    addresses = UserAddress.objects.filter(customer=user)
    return {'addresses':addresses}  

def product_context(request):
    products = Products.objects.all()
    colors = Color.objects.all()
    size = Size.objects.all()
    categories = Category.objects.all()
    context = {
        'productsss':products,
        'colors':colors,
        'sizes':size,
        'categories':categories
    }
    if products:
        return context
    else:
        return{}

def orders(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        user = Customer.objects.get(id = user_id)
        wish_count = Wishlist.objects.filter(customer=user).count()
        user_name = user.name
        user_email = user.email
        orders = Order.objects.filter(customer=user).order_by('-order_date')
        context = {
            'orders':orders,
            'user_name':user_name,
            'user_email':user_email,
            'wish':wish_count
        }
        
        return context
    else:
        return{}
 
 
