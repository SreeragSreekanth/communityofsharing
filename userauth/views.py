from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignupForm, LoginForm

# Signup View
def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, 'Registration successful!')
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    """Login View for existing users."""
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # If the user is a superuser and not approved, update their approval status
                if user.is_superuser and not user.is_approved:
                    user.is_approved = True  # Set user as approved
                    user.save()  # Save the changes to the database
                
                # Check if the user is approved
                if user.is_approved:
                    login(request, user)
                    
                    # Redirect based on user role
                    if user.is_superuser:
                        return redirect('admin_dashboard')  # Redirect to the admin dashboard
                    else:
                        return redirect('user_dashboard')  
                else:
                    messages.error(request, "Your account is not yet approved.")
            else:
                messages.error(request, "Invalid credentials or account not approved.")
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

# Logout View
def user_logout(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request, 'home.html')