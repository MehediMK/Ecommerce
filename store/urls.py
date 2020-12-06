from django.urls import path
from .views import Index,Signup,Login,logout,Cart,Checkout

urlpatterns = [
    path('',Index.as_view(),name='home'),
    path('signup/',Signup.as_view(),name='signup'),
    path('login/',Login.as_view(),name='login'),
    path('logout/',logout,name='logout'),
    path('cart/',Cart.as_view(),name='cart'),
    path('check-out',Checkout.as_view(),name='checkout'),
]
