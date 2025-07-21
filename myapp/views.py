import random
from django.shortcuts import  render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from myapp.models import Product,Cart,Buy,Review,Category
from myapp.forms import CartForm,ReviewForm
from myapp.myapp import *
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect

#login related imported
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.core.mail import send_mail
from django.shortcuts import render, redirect
import random
# Create your views here.
def category(request):
    c= Category.objects.all()
    context={'c':c}
    print(c)
    return render(request,'categories.html',context)
def products(request,product_id,slug):
    p=Product.objects.filter(category=product_id)
    if request.GET.get('q'):
        query=request.GET.get('q')
        p=Product.objects.filter(title__icontains=query)
    context={'p':p}
    return render(request,'index.html',context)
def detail(request,product_id,slug):
    d=Product.objects.get(id=product_id)
    if request.method=="POST":
        f=CartForm(request,request.POST)
        if f.is_valid():
            request.form_data=f.cleaned_data
            add_to_cart(request)
            return redirect('myapp:cart_view')

    f=CartForm(request,initial={'product_id':product_id})
    context={'d':d,'f':f}
    return render(request,'detail.html',context)
def cart_view(request):
    if request.method=="POST" and request.POST.get('delete')=='Delete':
        item_id=request.POST.get('item_id') 
        cd=Cart.objects.get(id=item_id)
        cd.delete()
    c=get_cart(request)
    t=total_(request)
    co=item_count(request)
    context={'c':c,'t':t}
    return render(request,'cart.html',context)
def order(request):
  # What you want the button to do.
  items=get_cart(request)
  for i in items:
    b=Buy(product_id=i.product_id,quantity=i.quantity,price=i.price)
    b.save()
    paypal_dict = {
        "business": "sb-u1vfe28146180@business.example.com",
        "amount": total_(request),
        "item_name": cart_id(request),
        "invoice": str(uuid.uuid4()),
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('myapp:return_view')),
        "cancel_return": request.build_absolute_uri(reverse('myapp:cancel_view')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form,"items":items,"total":total_(request)}
    return render(request, "order.html", context)
def return_view(request):
    return render(request,'transaction.html')
def cancel_view(request):
    return HttpResponse('Transaction Cancelled')
def review(request,product_id,pk):
    d=Product.objects.get(id=product_id)
    reviews = Review.objects.filter(post_id = product_id)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.cleaned_data['review']
            c = Review(post_id = product_id,review = review,user = request.user)
            c.save()
            
    else:
        form = ReviewForm()

    return render(request, 'review.html', {'d':d,'form': form,'reviews':reviews})



# ... other views (index, login, logout) ...
def send_otp(email, otp):
    subject = 'OTP Verification'
    message = f'Your OTP for registration is: {otp}'
    send_mail(subject, message, None, [email])


from django.http import HttpResponseRedirect

# ...

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('myapp:register')

        otp_number = random.randint(1000, 9999)
        otp = str(otp_number)

        send_otp(email, otp)
        request.session['username'] = username
        request.session['email'] = email
        request.session['password'] = password
        request.session['otp'] = otp  # Add this line to store OTP in the session

        # Construct the URL using HttpResponseRedirect
        #return HttpResponseRedirect(f'/otp/{otp}/{username}/{password}/{email}/')
        # Alternatively, you can use reverse:
        return HttpResponseRedirect(reverse('myapp:otp', args=[otp, username, password, email]))

    else:
        return render(request, 'register.html')


def otp(request, otp, username, password, email):
    if request.method == "POST":
        uotp = request.POST['otp']
        otp_from_session = request.session.get('otp')

        if uotp == otp_from_session:
            username = request.session.get('username')
            email = request.session.get('email')
            password = request.session.get('password')

            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return redirect('myapp:login')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('myapp:otp', otp=otp, username=username, password=password, email=email)

    return render(request, 'otp.html',{'otp': otp, 'username': username, 'password': password, 'email': email})



def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Invalid user credentials')
            return redirect('myapp:login')
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout (request)
    return redirect('/')
