from django.shortcuts import render , get_object_or_404
from .models import Product, Auth, CartItem
from django.contrib import messages
from django.shortcuts import redirect

#  register
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'Email and password are required.')
            return redirect('register')
        
        if Auth.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')
        
        user = Auth(email=email, password=password)
        user.save()
        
        messages.success(request, 'Registration Successful!')

        return redirect('login')
    
    return render(request, 'register.html')
    
# login
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'Email and password are required.')
            return redirect('login')
        
        elif not Auth.objects.filter(email=email, password=password).exists():
            messages.error(request, 'Invalid email or password.')
            return redirect('login')
     
        if Auth.objects.filter(email=email, password=password).exists():
            user = Auth.objects.get(email=email)
            request.session['user_id'] =  user.id  # Store user ID in session
            messages.success(request, 'Login Successful!')
            return redirect('home')
        
    return render(request, 'login.html')

# logout
def logout(request):
    if 'user_id' in request.session:
        request.session.flush()
        return redirect('home')

#  home
def home(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})    

# cart
def cart(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = get_object_or_404(Auth, id=user_id)
    cart_items = CartItem.objects.filter(user=user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    total_quantity = sum(item.quantity for item in cart_items)
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'total_quantity': total_quantity,
    })

def update_quantity(request, item_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.session.get('user_id')

        if not user_id:
            return redirect('home')
        
        user = get_object_or_404(Auth, id=user_id)
        product = get_object_or_404(Product, id=item_id)
        cart_item = get_object_or_404(CartItem, user=user, product=product)

        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()

        elif action == 'decrease' and cart_item.quantity <= 1:        
            cart_item.delete()
            
        elif action == 'decrease':
            cart_item.quantity -= 1
            cart_item.save()

        elif action == 'remove':
            cart_item.delete()

        return redirect('cart')
    
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    user = get_object_or_404(Auth, id=user_id)
    cart_item, created = CartItem.objects.get_or_create(
        user = user,
        product = product
    )
    if not created :
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

# add to cart
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_id = request.session.get('user_id')  

    if not user_id:
        return redirect('login') 

    user = get_object_or_404(Auth, id=user_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{product.name} updated in your cart.")
    return redirect('home')

def search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Product.objects.filter(name__icontains=query)
    
    return render(request, 'search_results.html', {'results': results, 'query': query})

# about
def about(request):
    return render(request, 'about.html')

# contact
def contact(request):
    return render(request, 'contact.html')

