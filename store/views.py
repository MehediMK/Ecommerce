from django.shortcuts import render,redirect,HttpResponseRedirect,get_object_or_404
from django.http import HttpResponse

from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.orders import Order
from .models.contact import ContactModel

from django.contrib.auth.hashers import make_password,check_password
from django.views import View
from .middlewares.auth import auth_middleware
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger




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

        # this query for pagination
        productview = request.GET.get('productview', 1)
        home_paginator = Paginator(products, 12)
        try:
            products_list = home_paginator.page(productview)
        except PageNotAnInteger:
            products_list = home_paginator.page(1)
        except EmptyPage:
            products_list = home_paginator.page(home_paginator.num_pages)
        # end pagination query

        context = {
            'products':products_list,
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


class ProductDetailView(View):
    def get(self,request,id):
        product = get_object_or_404(Product, id=id)
        context = {
            'product':product,
        }
        return render(request,'productdetailview.html',context)


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

class CustomerProfile(View):
    def get(self,request):
        customerid = request.session['customer']
        print(customerid)
        mycustomer = Customer.objects.get(id=int(customerid))
        print(mycustomer.first_name)
        context ={
            'customer':mycustomer,
        }
        return render(request,'customerProfile.html',context)

class Login(View):
    return_Url = None
    def get(self,request):
        Login.return_Url = request.GET.get('return_Url')
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

                if Login.return_Url:
                    return HttpResponseRedirect(Login.return_Url)
                else:
                    Login.return_Url = None
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
        mycart = request.session.get('cart')
        if mycart:
            ids = list(request.session.get('cart').keys())
            products = Product.get_product_by_id(ids)
            print(products)
            return render(request,'cart.html',{'products':products})
        else:
            request.session['cart'] = {}
            ids = list(request.session.get('cart').keys())
            products = Product.get_product_by_id(ids)
            print(products)
            return render(request,'cart.html',{'products':products})



class Checkout(View):
    def post(self,request):
        address = request.POST.get('address')
        bkashtrxid = request.POST.get('bkashtrxid')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_product_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products,bkashtrxid)

        for product in products:
            # print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          bkashTrxID=bkashtrxid,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()
            print(Customer(id=customer),product,product.price,address,phone,cart.get(str(product.id)),bkashtrxid)
        request.session['cart'] = {}

        return redirect('cart')


class OrderView(View):
    @method_decorator(auth_middleware)
    def get(self,request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer) 
        print(orders)
        return render(request,'orders.html',{'orders':orders})


class IncDec(View):
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
        return redirect('cart')


class ContactView(View):
    def get(self,request):
        return render(request,'contact.html')
    def post(self,request):
        re = request.POST
        fname = re.get('fname')
        lname = re.get('lname')
        email = re.get('email')
        phone = re.get('phone')
        comments = re.get('comments')
        if fname != '' and lname != '' and email != '' and phone != '' and comments != '':
            print(fname,lname,email,phone,comments)
            contact = ContactModel.objects.create(fname=fname,lname=lname,email=email,phone=phone,comments=comments)
            contact.save()
            return redirect('home')
        else:
            return render(request,'contact.html')


class AboutUsView(View):
    def get(self,request):
        return render(request,'aboutus.html')

def pymentoptionview(request):
    return render(request,'pymentoption.html')


class ProductSearch(View):
    def get(self,request):  
        context = {}  
        search = request.POST.get('search')    
        mysearch = request.GET.get('search')
        context['mysearch'] = mysearch

        # here check cart empty or not
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}

        products = None

        categories = Category.get_all_category()
        context['categorys'] = categories

        categoryID = request.GET.get('category')
        message = None
        # here get product by search name
        if mysearch:
            myproductsearch = Product.objects.filter(name__icontains=mysearch)
            if myproductsearch:
                products=myproductsearch
            else:
                message = 'Search not found'
        else:
            if categoryID:
                products = Product.get_all_products_by_categoryid(categoryID)
            else:
                products = Product.get_all_products()
        # here check froduct or not th
        if message:
            context['message'] = message
        else:
            # this query for pagination
            productview = request.GET.get('productview', 1)
            home_paginator = Paginator(products, 12)
            try:
                products_list = home_paginator.page(productview)
                context['products'] = products_list
            except PageNotAnInteger:
                products_list = home_paginator.page(1)
                context['products'] = products_list
            except EmptyPage:
                products_list = home_paginator.page(home_paginator.num_pages)
                context['products'] = products_list
            # end pagination query
            
        print('your are: ',request.session.get('customer'))

        return render(request,'ProductSearch.html',context)


    def post(self,request):
        product = request.POST.get('productid')
        remove = request.POST.get('remove')
        search = request.POST.get('search')
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
        return HttpResponseRedirect(f'?search={search}') 

