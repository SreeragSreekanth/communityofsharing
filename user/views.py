from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from userauth.models import Profile
from userauth.forms import EditProfileForm
from django.contrib import messages
from django.contrib.auth import get_user_model


User = get_user_model()

# User Dashboard View
@login_required
def user_dashboard(request):
    # Fetch the user's profile
    profile = request.user.profile
    context = {'profile': profile}
    return render(request, 'user_dashboard.html', context)

# Edit Profile View
@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            if form.cleaned_data.get('remove_picture'):  # Check if the user wants to remove the image
                profile.profile_picture.delete(save=False)  # Delete the image file
                profile.profile_picture = None 
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('user_dashboard')
    else:
        form = EditProfileForm(instance=profile)
    
    context = {'form': form,'profile': profile}
    return render(request, 'edit_profile.html', context)

@login_required
def view_profile(request, user_id):
    # Fetch the user by ID or return a 404 error if not found
    user = get_object_or_404(User, id=user_id)
    profile = user.profile  # Access the related Profile model
    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'view_profile.html', context)