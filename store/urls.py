from django.urls import path
from .views import Index,Signup,Login,logout,Cart,Checkout,OrderView,IncDec

urlpatterns = [
    path('',Index.as_view(),name='home'),
    path('signup/',Signup.as_view(),name='signup'),
    path('login/',Login.as_view(),name='login'),
    path('logout/',logout,name='logout'),
    path('cart/',Cart.as_view(),name='cart'),
    path('check-out',Checkout.as_view(),name='checkout'),
    path('order',OrderView.as_view(),name='order'),
    path('incdec',IncDec.as_view(),name='incdec'),
]
