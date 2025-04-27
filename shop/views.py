from django.shortcuts import render, redirect, get_object_or_404
from .models import ProductColor, Products,Order,History, SpareEntry, AdminUser
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
from django.utils.timezone import now
import ast
import json
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
# from cryptography.fernet import Fernet
import base64
from django.conf import settings
from shop.models import Users
from django.views.decorators.csrf import csrf_exempt
from authenticationlogin.models import AuthenticatedUser
from shop.models import WebsiteLogo
from authenticationlogin.decorators import login_required_custom
from django.contrib.auth.decorators import login_required





# Create your views here.
@login_required_custom 
def index(request):
    product_objects = Products.objects.all()
    product_list = Products.objects.all().order_by('id')  # ✅ Initialize product_list first

    query = request.GET.get('item_name','')
    if query:
        product_list=product_list.filter(title__icontains=query)
    #search code
    item_name = request.GET.get('item_name')
    if item_name != '' and item_name is not None:
        product_objects = product_objects.filter(title__icontains=item_name)
 
    #paginator code
    # product_list = Products.objects.all().order_by('id')  # Orders by ID to ensure consistency

    paginator = Paginator(product_list,10)
    page = request.GET.get('page')
    product_objects = paginator.get_page(page)
    
    return render(request,'shop/index.html',{'product_objects':product_objects, 'query': query})
 
@login_required_custom 
def detail(request,id):
    product_object = Products.objects.get(id=id)
    return render(request,'shop/detail.html',{'product_object':product_object})
@login_required_custom    
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

# from django.shortcuts import render
# from .models import Products

@login_required(login_url='/dashboard_login/')
def dashboard(request):
    # logo = WebsiteLogo.objects.last()
    # form = LogoUploadForm()
    users = AuthenticatedUser.objects.all()
    # return render(request, 'shop/dashboard.html', {'users': users})
    # Store encrypted_password in a separate field in the database
    if request.user.is_authenticated:
        pass  # Allow access

    # Check if session contains an admin user (from custom model)
    elif "admin_user" not in request.session:
        return redirect("dashboard_login")  # Redirect to login if not logged in

    if request.method == "POST":
        title = request.POST.get("title")
        price = request.POST.get("price")
        description = request.POST.get("description")
        image = request.POST.get("image")  # Get the image URL
        stock = int(request.POST.get("stock", 0))  # Get stock value


        # Save product
        discount_price = request.POST.get("discount_price", 0)  # Default to 0 if not provided

        new_product = Products(title=title, price=price, description=description, image=image, discount_price=discount_price, stock=stock)
        new_product.save()

        return redirect("dashboard")  # Redirect to avoid duplicate submissions

    product_objects = Products.objects.all()
    from django.contrib.auth.models import User

    admin_users = User.objects.all()  # Fetch all admin users

    return render(request, "shop/dashboard.html", { "product_objects": product_objects})

def delete_product(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    product.delete()
    return redirect('dashboard')  # Redirect back to the dashboard

def edit_product(request, product_id):
    product = get_object_or_404(Products, id=product_id)

    if request.method == "POST":
        product.title = request.POST.get("title")
        product.price = request.POST.get("price")
        product.discount_price = request.POST.get("discount_price", 0)
        product.description = request.POST.get("description")
        product.image = request.POST.get("image")
        product.stock = request.POST.get("stock")
        product.save()
        return redirect('dashboard')  # Redirect to dashboard after saving

    return render(request, 'shop/edit_product.html', {'product': product})


@login_required_custom
# Cart Logic
def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = Products.objects.get(id=product_id)
        total_price = product.price * quantity
        cart_items.append({'product': product, 'quantity': quantity, 'total_price': total_price})
        total += total_price

    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total': total})



def add_to_cart(request, product_id, quantity):
    """Handles adding products to cart and ensures quantity is stored correctly as an integer."""
    
    cart = request.session.get("cart", {})

    product_id = str(product_id)  # Ensure product ID is a string
    quantity = int(quantity)  # Ensure quantity is an integer
    product = get_object_or_404(Products, id=product_id)
    current_qty = cart.get(product_id, 0)

    if current_qty + quantity > product.stock:
        return JsonResponse({
            "error": "Cannot add more than stock",
            "cart_count": sum(cart.values()),
            "product_stock": product.stock,
            "in_cart": current_qty
        })

    cart[product_id] = current_qty + quantity
    request.session["cart"] = cart
    request.session.modified = True

    return JsonResponse({
        "success": True,
        "cart_count": sum(cart.values()),
        "new_qty": cart[product_id],
        "product_stock": product.stock
    })

    # ✅ Ensure cart stores only integers for quantity
    if product_id in cart and isinstance(cart[product_id], int):
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity  # ✅ Store only as integer

    request.session["cart"] = cart
    request.session.modified = True

    # ✅ Fix: Sum only integer values
    cart_count = sum(qty for qty in cart.values() if isinstance(qty, int))

    return JsonResponse({"cart_count": cart_count})

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        del cart[str(product_id)]  # Remove the product from the cart

    request.session['cart'] = cart
    request.session.modified = True
    return JsonResponse({'cart_count': sum(cart.values())})

def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})

    product = Products.objects.get(id=product_id)
    current_qty = cart.get(str(product_id), 0)

    # Only increase if quantity is less than stock
    if current_qty < product.stock:
        cart[str(product_id)] = current_qty + 1

    request.session['cart'] = cart
    request.session.modified = True

    new_qty = cart[str(product_id)]
    new_total = product.price * new_qty
    grand_total = sum(
        Products.objects.get(id=int(pid)).price * qty for pid, qty in cart.items()
    )

    return JsonResponse({
        'cart_count': sum(cart.values()),
        'new_qty': new_qty,
        'new_total': new_total,
        'grand_total': grand_total,
        'max_reached': new_qty >= product.stock  # optional flag for frontend
    })


def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        if cart[str(product_id)] > 1:
            cart[str(product_id)] -= 1
        else:
            del cart[str(product_id)]  # Remove item if quantity reaches 0

    request.session['cart'] = cart
    request.session.modified = True

    new_qty = cart.get(str(product_id), 0)
    product = Products.objects.get(id=product_id) if new_qty > 0 else None
    new_total = product.price * new_qty if product else 0
    grand_total = sum(Products.objects.get(id=int(pid)).price * qty for pid, qty in cart.items())


    return JsonResponse({
        'cart_count': sum(cart.values()),
        'new_qty': new_qty,
        'new_total': new_total,
        'grand_total': grand_total

    })

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session['cart'] = cart
    request.session.modified = True

    grand_total = sum(Products.objects.get(id=int(pid)).price * qty for pid, qty in cart.items())

    return JsonResponse({
        'cart_count': sum(cart.values()),
        'grand_total': grand_total
    })



def get_cart_count(request):
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    return JsonResponse({'cart_count': cart_count})


def cart_total(request):
    cart = request.session.get("cart", {})
    total = sum(Products.objects.get(id=int(pid)).price * qty for pid, qty in cart.items())

    return JsonResponse({"total": total})

@login_required_custom
def spare(request):
    products = Products.objects.all()
    spare_entries = SpareEntry.objects.all().order_by('-timestamp')  # Fetch all actions, latest first


    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity"))
        action = request.POST.get("action")

        product = Products.objects.get(id=product_id)

        if action == "returned":
            product.stock += quantity  # Increase stock
            messages.success(request, f"{quantity} units added to {product.title}'s stock.")
        elif action == "destroyed":
            if product.stock >= quantity:
                product.stock -= quantity  # Reduce stock
                messages.success(request, f"{quantity} units removed from {product.title}'s stock.")
            else:
                messages.error(request, "Not enough stock to destroy that quantity.")
                return redirect('spare')

        product.save()
        SpareEntry.objects.create(product=product, quantity=quantity, action=action)

        return redirect('spare')

    return render(request, 'shop/spare.html', {'products': products, 'spare_entries': spare_entries})

# from django.shortcuts import render
# from django.shortcuts import render
# from .models import Products

@login_required_custom
def finalize_order(request):
    # Get order details from form
    name = request.POST.get("name")
    mobile = request.POST.get("mobile")
    address = request.POST.get("address")
    id_number = request.POST.get("id_number", "")
    notes = request.POST.get("notes", "")  # ✅ Capture notes from form
    tax_selection = request.POST.get("tax")

    cart = request.session.get("cart", {})  # Retrieve cart from session
    if not cart:
        messages.error(request, "Your cart is empty!")
        return redirect('cart')
    cart_items = []
    total = 0
    # updated_products = set()

    # Retrieve product details from the database
    for product_id, quantity in cart.items():
        try:
            product = Products.objects.get(id=int(product_id))
            

            total_price = product.price * quantity
            cart_items.append({
                "id": product.id,  # ✅ Add product ID
                "name": product.title,
                "quantity": quantity,
                "unitPrice": product.price,
                "totalPrice": total_price
            })
            total += total_price
        except Products.DoesNotExist:
            continue  # Skip products that no longer exist
    
    if request.method == "POST":
         # Apply tax if selected
        if tax_selection == "tax":
            tax_amount = total * 0.14
            total += tax_amount

        # Save order in the History table instead of Order
        history = History.objects.create(
            name=name,
            mobile=mobile,
            address=address,
            id_number=id_number,
            notes=notes,  # ✅ Save notes
            items=json.dumps(cart_items),  # Store items as a JSON string
            total=total
        )


        for item in cart_items:
            try:
                product = Products.objects.get(id=item["id"])
                product.stock -= item["quantity"]  # ✅ Reduce stock exactly by the ordered quantity
                product.save()  # ✅ Save the updated stock

            except Products.DoesNotExist:
                continue  # If a product is missing, skip it


        # Clear the cart after placing the order
        request.session['cart'] = {}
        request.session.modified = True

        

        return redirect('receipt', order_id=history.id)

        

    return render(request, "shop/finalize_order.html", {"cart_items": cart_items, "total": total})
@login_required_custom
def receipt(request, order_id):
    order = get_object_or_404(History, id=order_id)
    order.items_list = ast.literal_eval(order.items)  # Convert string back to list

    return render(request, "shop/receipt.html", {"order": order})
@login_required_custom
def receipts(request):
    search_query = request.GET.get('search_query', '')

    # Show most recent 10 receipts by default
    orders = History.objects.all().order_by('-created_at')

    # Filter by Name or Date if a search query is entered
    if search_query:
        if "-" in search_query:  # If the user entered a date (YYYY-MM-DD)
            orders = orders.filter(created_at__date=search_query)
        else:  # Otherwise, filter by name
            orders = orders.filter(name__icontains=search_query)

    # Paginate results (10 per page)
    paginator = Paginator(orders, 10)
    page = request.GET.get('page')
    orders = paginator.get_page(page)

    return render(request, 'shop/receipts.html', {'orders': orders, 'search_query': search_query})
@login_required_custom
def coming_soon(request):
    return render(request, "shop/coming_soon.html")

def dashboard_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # ✅ This must match the name used in your urls.py
        else:
            return render(request, "shop/dashboard_login.html", {"error_message": "Invalid credentials."})

    return render(request, "shop/dashboard_login.html")



def change_stock(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity"))
        
        products = Products.objects.get(id=product_id)
        products.stock += quantity
        products.save()

        return redirect('dashboard')  # Redirect back to dashboard after updating stock


    products = Products.objects.all()
    return render(request, "shop/change_stock.html", {"products": products})




#thank you for seeing my work look out for more , love # aly 