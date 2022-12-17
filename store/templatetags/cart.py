from django import template
from datetime import  timedelta
from store.models import *

register = template.Library()


@register.filter(name = 'is_in_cart')
def is_in_cart(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return True
    
    return 0

@register.filter(name = 'cart_quantity')
def cart_quantity(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)
    
    return 0

@register.filter(name = 'price_total')
def price_total(product, cart):
    return (offer_price(product)) * cart_quantity(product, cart)

@register.filter(name = 'price_total_without_discount')
def price_total_without_discount(product, cart):
    return (offer_price(product)+discount(product)) * cart_quantity(product, cart)


@register.filter(name = 'total_cart_price')
def total_cart_price(products, cart):
    sum = 0
    for p in products:
        sum += price_total(p, cart)   
    return sum

@register.filter(name = 'total_cart_price_discount')
def total_cart_price_discount(products, cart):
    sum = 0
    for p in products:
        sum += (offer_price(p)+discount(p)) * cart_quantity(p, cart)  
    return sum

@register.filter(name = 'is_in_wish')
def is_in_wish(product, user_id):
    user = Customer.objects.get(id = user_id)
    products = Wishlist.objects.filter(customer = user, product = product)
    for wish in products:
        if wish.product == product: 
            return True
        else:
            return False


@register.filter(name = 'return_date')
def return_date(order_date):
    return_date = order_date.date() + timedelta(days=7)

    return return_date


@register.filter(name = 'check_offer')
def check_offer(product):
    product_offer = ProductOffer.objects.all()
    category_offer = CategoryOffer.objects.all()
    offer = False
    for offers in product_offer:
        if product == offers.product and offers.is_expired == False:
            offer = True
            break

    for offers in category_offer:
        if product.category == offers.category and offers.is_expired == False:
            offer = True  
            break      
    
    return offer





@register.filter(name = 'check_discount')
def check_discount(product):
    product_offer = ProductOffer.objects.all()
    category_offer = CategoryOffer.objects.all()

    product_offer_price = 0
    category_offer_price = 0
    product_dis = 0
    category_dis =0
    for offers in product_offer:
        if product == offers.product:
          
            product_discount_type = offers.discount_type
            
            if product_discount_type == 'FLAT':
                product_dis = offers.discount
                
                product_offer_price = 'Flat ₹'+str(offers.discount)+' off'
            else:
                product_dis = product.price * (offers.discount/100)
                product_offer_price = str(offers.discount)+"% off" 
  

    for offers in category_offer:
   
        if product.category == offers.category:
       
            category_discount_type = offers.discount_type
            
            if category_discount_type =='FLAT':
                category_dis = offers.discount
                category_offer_price = 'Flat ₹'+str(offers.discount)+' off'
            else:
                category_dis = product.price * (offers.discount/100)
                category_offer_price = str(offers.discount)+"% off"
          
            
    # if product_dis == 0 and category_dis == 0:
    #     discount = 0
        
    if product_dis > category_dis:
        discount = product_offer_price
    
    else:
        discount = category_offer_price
    
        
    return discount


@register.filter(name = 'offer_price')
def offer_price(product):
    product_offer = ProductOffer.objects.all()
    category_offer = CategoryOffer.objects.all()
    price = product.price
    product_offer_price = 0
    category_offer_price = 0
    product_dis = 0
    category_dis =0
    for offers in product_offer:
        if product == offers.product:
            product_discount_type = offers.discount_type

            if product_discount_type == 'FLAT':
                product_dis = offers.discount
                product_offer_price = product.price-product_dis
            else:
                product_dis = product.price * (offers.discount/100)
                product_offer_price = product.price-product_dis


    for offers in category_offer:
        if product.category == offers.category:

            category_discount_type = offers.discount_type
            if category_discount_type =='FLAT':
                category_dis = offers.discount
            else:
                category_dis = product.price * (offers.discount/100)
            category_offer_price = product.price-category_dis
    
    if product_dis == 0 and category_dis == 0:
        return price

    elif product_dis > category_dis:
        return product_offer_price

    else:
        return category_offer_price



@register.filter(name = 'discount')
def discount(product):
    product_offer = ProductOffer.objects.all()
    category_offer = CategoryOffer.objects.all()
    discount = product.price
    product_offer_price = 0
    category_offer_price = 0
    product_dis = 0
    category_dis =0
    for offers in product_offer:
        if product == offers.product and not offers.is_expired:
            product_discount_type = offers.discount_type
            
            if product_discount_type == 'FLAT':
                product_dis = offers.discount
            else:
                product_dis = product.price * (offers.discount/100)
                
  

    for offers in category_offer:
        if product.category == offers.category:
            
            category_discount_type = offers.discount_type
            if category_discount_type =='FLAT':
                category_dis = offers.discount
            
            else:
                category_dis = product.price * offers.discount/100          
        
    if product_dis > category_dis:
        discount = product_dis
    
    else:
        discount =  category_dis
    return discount



@register.filter(name = 'total_discount')
def total_discount(products,cart):  
    sum = 0
    for p in products:
        sum += discount(p) * cart_quantity(p, cart)  
    return sum