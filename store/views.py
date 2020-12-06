from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.orders import Order
from django.contrib.auth.hashers import make_password,check_password
from django.views import View


# video 53 running

class Index(View):
    def get(self,request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        products = None
        categories = Category.get_all_category()
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        else:
            products = Product.get_all_products()

        context = {
            'products':products,
            'categorys':categories
        }
        print('your are: ',request.session.get('customer'))
        return render(request,'index.html',context)


    def post(self,request):
        product = request.POST.get('productid')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        print(request.session['cart'])
        return redirect('home')


class Signup(View):
    def get(self,request):
        return render(request,'signup.html')
    def post(self,request):
        requestData = request.POST
        fname = requestData.get('fname')
        lname = requestData.get('lname')
        phone = requestData.get('phone')
        email = requestData.get('email')
        password = requestData.get('password')
        data = {
            'fname':fname,
            'lname':lname,
            'phone':phone,
            'email':email,
        }
        customer = Customer(first_name=fname,last_name=lname,phone=phone,email=email,password=password)
        error = dict()
        if not fname:
            error['fname'] = "First name empty."
        elif len(fname)<4:
            error['fname'] = "First name less than 4 charecter."
        if not lname:
            error['lname'] = 'Last name is empty.'
        elif len(lname)<4:
            error['lname'] = 'last name less than 4 charecter.'
        if not phone:
            error['phone'] = 'phone number empty.'
        elif len(phone)<11:
            error['phone'] = 'phone number less then 11 character.'
        if not email:
            error['email'] = 'email address is empty.'
        if not password:
            error['password'] = 'please enter your password'
        elif len(password)<8:
            error['password'] = 'Password less then 8 character.'
        
        isExits = customer.isExits()
        if isExits:
            error['register'] = 'Email Already registered.'

        if not error:
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('home')
        else:
            context = {
                'value':data,
                'error':error,
            }
            return render(request,'signup.html',context)


class Login(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        error = None
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        
        if customer:
            flag = check_password(password,customer.password)
            print(flag)
            if flag:
                request.session['customer'] = customer.id
                
                return redirect('home')
            else:
                error = "You enter wrong email or password."
                return render(request,'login.html',{'error':error})
        else:
            error = "You enter wrong email or password."
            return render(request,'login.html',{'error':error})


def logout(request):
    request.session.clear()
    return redirect('login')


class Cart(View):
    def get(self,request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_product_by_id(ids)
        print(products)
        return render(request,'cart.html',{'products':products})


class Checkout(View):
    def post(self,request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_product_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)

        for product in products:
            # print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()
            print(Customer(id=customer),product,product.price,address,phone,cart.get(str(product.id)))
        request.session['cart'] = {}

        return redirect('cart')


class OrderView(View):
    def get(self,request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request,'orders.html',{'orders':orders})





