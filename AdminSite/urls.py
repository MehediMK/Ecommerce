from django.urls import path
from .views import DashboardView,AdminProfile,AdminLogin,AdminLogout,AddCategory,AddProduct

urlpatterns = [
    path('',DashboardView.as_view(),name='dashboard'),
    path('adminprofile/',AdminProfile.as_view(),name='adminprofile'),
    path('adminlogin/',AdminLogin.as_view(),name='adminlogin'),
    path('adminlogout/',AdminLogout.as_view(),name='adminlogout'),
    path('addcategory/',AddCategory.as_view(),name='addcategory'),
    path('addproduct/',AddProduct.as_view(),name='addproduct'),
]
