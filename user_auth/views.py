from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib import messages
#password hashing
from django.contrib.auth.hashers import make_password, check_password
from .models import User_auth
# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password)
            user.save()
            messages.success(request, "You have been signed up successfully!")
            return redirect('profile_views')
        else:
            messages.error(request, "Please correct the errors below.")
            return redirect('signup')
    return render(request, 'signup.html', {"form": SignupForm()})


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User_auth.objects.get(email=email)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                messages.success(request, "You have been logged in successfully!")
                return redirect('profile_views')
            else:
                messages.error(request, "Invalid password.")
                return redirect('login')
        except User_auth.DoesNotExist:
            messages.error(request, "User with this email does not exist.")
            return redirect('login')
    return render(request, 'login.html')
