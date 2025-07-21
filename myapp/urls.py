from django.urls import path
from myapp.views import order,products,detail,cart_view,return_view,cancel_view,review,category,register,login,logout,otp
app_name='myapp'

urlpatterns = [
path('',category,name='category'),
path('products/<int:product_id>/<slug:slug>',products,name='products'),
path('<int:product_id>/<slug:slug>',detail,name='detail'),
path('cart/',cart_view,name='cart_view'),
path('order/',order,name='order'),
path('success/',return_view,name='return_view'),
path('cancel/',cancel_view,name='cancel_view'),
path('<int:product_id>/<int:pk>/review/',review,name='review'),
path('register',register,name="register"),
path('login',login,name="login"),
path('logout',logout,name="logout"),
path('otp/<str:otp>/<str:username>/<str:password>/<str:email>/',otp, name='otp'),
]