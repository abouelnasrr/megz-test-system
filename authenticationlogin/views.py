from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm, LoginForm
from .models import AuthenticatedUser, LoginSession
from shop.models import AdminUser, WebsiteLogo
from django.views.decorators.http import require_POST
from authenticationlogin.forms import LogoUploadForm
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from shop.models import AdminUser, Users
from django.utils import timezone
from django.core.paginator import Paginator



def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'authenticationlogin/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = AuthenticatedUser.objects.filter(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            ).first()
            if user:
                request.session['user_id'] = user.id
                request.session['username'] = user.username

                # ✅ Save login session
                session = LoginSession.objects.create(user=user)
                request.session['session_id'] = session.id

                return redirect('index')
            else:
                form.add_error(None, "Invalid credentials")
    else:
        form = LoginForm()
    return render(request, 'authenticationlogin/login.html', {'form': form})



def logout_view(request):
    session_id = request.session.get('session_id')
    if session_id:
        try:
            session = LoginSession.objects.get(id=session_id)
            session.logout_time = timezone.now()
            session.save()
        except LoginSession.DoesNotExist:
            pass
    request.session.flush()
    return redirect('login')


def users_dashboard(request):
    admin_users = User.objects.all()
    users = AuthenticatedUser.objects.all()
    logo = WebsiteLogo.objects.last()
    sessions = LoginSession.objects.select_related('user').order_by('-login_time')

    return render(request, 'authenticationlogin/users_dashboard.html', {
        'logo': logo,
        'form': LogoUploadForm, 
        "admin_users": admin_users,
        "users": users,
        "sessions": sessions

    })

@require_POST
def upload_logo(request):
    form = LogoUploadForm(request.POST, request.FILES)
    if form.is_valid():
        WebsiteLogo.objects.all().delete()  # Remove previous logos
        form.save()
    return redirect('users_dashboard')


def remove_logo(request):
    WebsiteLogo.objects.all().delete()
    return redirect('users_dashboard')

from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def add_admin_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        is_superuser = request.POST.get("is_superuser") == "on"

        if password != confirm_password:
            return render(request, "authenticationlogin/users_dashboard.html", {
                "error_message": "Passwords do not match."
            })

        # ✅ Check if user already exists
        if User.objects.filter(username=username).exists():
            return render(request, "authenticationlogin/users_dashboard.html", {
                "error_message": "Username already exists."
            })

        # ✅ Create user safely
        user = User.objects.create_user(
            username=username,
            password=password
        )
        user.is_superuser = is_superuser
        user.is_staff = is_superuser
        user.save()

        return redirect('users_dashboard')



# def get_plaintext_password(request, user_id):
#     user = user.objects.get(id=user_id)
#     return JsonResponse({'password': user.password})


def get_plaintext_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return JsonResponse({'password': user.password})

def delete_admin_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        messages.success(request, "User deleted successfully.")
    except User.DoesNotExist:
        messages.error(request, "User not found.")
    return redirect('users_dashboard')  

