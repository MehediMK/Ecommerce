from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView,View
from store.models import category,orders,product,customer
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib.auth import authenticate,login,logout
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .forms import AddCategoryForm,AddProductForm


class DashboardView(View):
    def get(self,request):
        customers = customer.Customer.objects.all()

        # this query for category
        categorys = category.Category.objects.all()
        category_page = request.GET.get('categorypage', 1)
        category_paginator = Paginator(categorys, 5)
        try:
            category_list = category_paginator.page(category_page)
        except PageNotAnInteger:
            category_list = category_paginator.page(1)
        except EmptyPage:
            category_list = category_paginator.page(category_paginator.num_pages)

        # this query for order
        myorders = orders.Order.objects.all()
        order_page = request.GET.get('orderpage', 1)
        order_paginator = Paginator(myorders, 5)
        try:
            order_list = order_paginator.page(order_page)
        except PageNotAnInteger:
            order_list = order_paginator.page(1)
        except EmptyPage:
            order_list = order_paginator.page(order_paginator.num_pages)

        # this query for products
        products = product.Product.objects.all()       
        page1 = request.GET.get('page', 1)
        paginator = Paginator(products, 5)
        try:
            products_list = paginator.page(page1)
        except PageNotAnInteger:
            products_list = paginator.page(1)
        except EmptyPage:
            products_list = paginator.page(paginator.num_pages)


        context = {
            'customers':customers,
            'categorys':category_list,
            'orders':order_list,
            'products':products_list, #pagination done
        }
        return render(request,'dashboard.html',context)


class AdminProfile(View):
    def get(self,request):
        return render(request,'user.html')


class AdminLogin(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return render(request,'auth/adminlogin.html')
        else:
            return redirect('/adminsite')
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/adminsite')
        else:
            return render(request,'auth/adminlogin.html')

class AdminLogout(View):
    def get(self,request):
        logout(request)
        return redirect('/adminsite')

class AddCategory(CreateView):
    model = category.Category
    form_class  = AddCategoryForm
    template_name = 'CRUD/addcategory.html'
    success_url = '/adminsite'

class AddProduct(CreateView):
    model = product.Product
    form_class = AddProductForm
    template_name = 'CRUD/addproduct.html'
    success_url = '/adminsite'


class CategoryDelete(View):
    def get(self,request,id):
        data = get_object_or_404(category.Category, id=id)
        data.delete()
        return redirect('/adminsite')

class ProductDelete(View):
    def get(self,request,id):
        data = get_object_or_404(product.Product, id=id)
        data.delete()
        return redirect('/adminsite')






