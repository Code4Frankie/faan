from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from hod.models import User

def profile(request):
    # Check if user_id is in session
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        
        if request.method == 'POST':
            # Handle form submission to update profile
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            new_password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            # Update user's profile
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            
            # Validate and hash the new password if provided
            if new_password:
                # Check if new password and confirm password match
                if new_password == confirm_password:
                    # Hash the new password before saving
                    hashed_password = make_password(new_password)
                    user.password = hashed_password
                    # Update password_changed to True
                    user.password_changed = True
                else:
                    messages.error(request, 'Passwords do not match. Please try again.')
                    return render(request, 'profile.html', {'user': user})

            user.save()
            messages.success(request, 'Profile updated successfully.')
            # Redirect to user_dashboard if password changed
            if user.password_changed:
                return redirect('dashboard')
        
        return render(request, 'profile.html', {'user': user})
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
