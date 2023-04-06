from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth,messages
from .models import Products,Order
from django.core.paginator import Paginator
# Create your views here.

def signup(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(username = request.POST['username'])
                return render (request,'shop/signup.html', {'error':'Username is already taken!'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                auth.login(request,user)
                return redirect('login')
        else:
            return render (request,'shop/signup.html', {'error':'Password does not match!'})
    else:
        return render(request,'shop/signup.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password = request.POST['password'])
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            return render (request,'shop/login.html', {'error':'Username or password is incorrect!'})
    else:
        return render(request,'shop/login.html')

def logout(request):
    if request.method == 'POST':
        messages.info(request, "You have successfully logged out.") 
        auth.logout(request)
    return redirect('signup')




def index(request):
    product_objects = Products.objects.all()

    #search code
    item_name = request.GET.get('item_name')
    if item_name != '' and item_name is not None:
        product_objects = product_objects.filter(title__icontains=item_name)

    #paginator code
    """ paginator = Paginator(product_objects,4)
    page = request.GET.get('page')
    product_objects = paginator.get_page(page) """
    
    return render(request,'shop/index.html',{'product_objects':product_objects})


def detail(request,id):
    product_object = Products.objects.get(id=id)
    return render(request,'shop/detail.html',{'product_object':product_object})
    
def checkout(request):

    if request.method == "POST":
        items = request.POST.get('items','')
        name = request.POST.get('name',"")
        email = request.POST.get('email',"")
        address = request.POST.get('address',"")
        city = request.POST.get('city',"")
        state =request.POST.get('state',"")
        zipcode = request.POST.get('zipcode',"")
        total = request.POST.get('total',"")
        order = Order(items=items,name=name,email=email,address=address,city=city,state=state,zipcode=zipcode,total=total)
        order.save()

    return render(request,'shop/checkout.html')
 