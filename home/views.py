from django.shortcuts import render, redirect
from .models import Product, CartItem, Order
from .forms import ProductForm, ContactForm, RegistrationForm, OrderForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.

def home(request):
    products = Product.objects.all()
    
    p = Paginator(products, 2)
    page_number = request.GET.get('page')

    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    try:
        items_in_cart = len(CartItem.objects.filter(user=request.user))
    except:
        items_in_cart = 0

    return render(request, "home/index2.html", {"page_obj" : page_obj, "items_in_cart":items_in_cart} )

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("contact")
    form = ContactForm()
    return render(request, "home/contact.html", {"contact_form": form})

def products(request):
    return render(request, "home/products.html")

@login_required(login_url='login')
def about(request):

    try:
        items_in_cart = len(CartItem.objects.filter(user=request.user))
    except:
        items_in_cart = 0

    return render(request, "home/about.html", {"items_in_cart":items_in_cart})


def product_detail(request, id):
    product = Product.objects.get(id=id)

    try:
        items_in_cart = len(CartItem.objects.filter(user=request.user))
    except:
        items_in_cart = 0

    context = {"product":product, "items_in_cart":items_in_cart}
    return render(request, "home/product_detail.html", context)

def form(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home_page")
    forms = ProductForm()
    context = {"forms":forms}
    return render(request, "home/form.html", context)

def signup(request):
    if request.method == "POST":
        user = RegistrationForm(request.POST, request.FILES)
        if user.is_valid():
            user.save()
        username = request.POST['username']
        password = request.POST['password1']
        u = authenticate(request, username=username, password=password)

        if u is not None:
            form = login(request, u)
            return redirect('/')

    form = RegistrationForm()
    context = {"form": form}
    return render(request, "home/signup.html", context)

@login_required(login_url="login")
def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    cart_item, create = CartItem.objects.get_or_create(product=product, user=request.user)
    cart_item.quantity += 1
    cart_item.price = product.price * cart_item.quantity
    cart_item.save()


    return redirect("/")

@login_required(login_url="login")
def cart(request):
    cart_item = CartItem.objects.filter(user=request.user)
    total = 0
    for i in cart_item:
        total += i.price

    try:
        items_in_cart = len(CartItem.objects.filter(user=request.user))
    except:
        items_in_cart = 0

    context = {"cart_items": cart_item, "total_price": total, "items_in_cart": items_in_cart}
    return render(request, "home/cart.html", context)

@login_required(login_url="login")
def remove_from_cart(request, id):
    cart_item = CartItem.objects.filter(id=id, user=request.user)
    cart_item.delete()
    return redirect('view_cart')

def checkout(request):
    if request.method == "POST":
        cart_item = CartItem.objects.filter(user=request.user)
        for item in cart_item:
            order = Order()
            order.name = request.POST.get("name")
            order.address = request.POST.get("address")
            order.phone = request.POST.get("phone")
            order.user = request.user
            order.quantity = item.quantity
            order.price = item.price
            order.product = item.product.name
            order.save() 

        for item in cart_item:
            item.delete()

        return redirect("/")   
            

    cart_item = CartItem.objects.filter(user=request.user)
    form = OrderForm()

    total = 0
    for i in cart_item:
        total += i.price

    products = []

    context = {"products": cart_item, "total_price": total, "form":form}
    print(context)

    return render(request, "home/checkout.html", context)