from django.shortcuts import render, redirect
from django.contrib import messages
from admin_area.models import HOD
from ..models import User
from django.core.mail import EmailMessage
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.hashers import make_password

def hod_add_users(request):
    if 'hod_id' in request.session:
        hod_id = request.session['hod_id']
        hod = HOD.objects.get(id=hod_id)

        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')

            # Assuming department is already set in the session
            department = hod.department

            # Hash the password
            hashed_password = make_password(password)

            # Create the new user
            new_user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=hashed_password,
                department=department
            )

            # Send email to the new user
            # send_user_email(new_user)

            messages.success(request, 'User added successfully.')
            return redirect('hod_dashboard')

        return render(request, 'hod_add_users.html', {'hod': hod})
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')

"""
def send_user_email(user):
    subject = 'Welcome to ' + user.department.name + ' Department'
    message = 'Dear ' + user.first_name + ',\n\nYou have been added to the ' + user.department.name + ' Department.\n\nPlease use the following credentials to login:\n\nEmail: ' + user.email + '\nPassword: ' + user.password + '\n\nAfter logging in, you will be asked to change your password.\n\nBest regards,\nFAAN\n\n'
    
    # Add login page link
    login_url = settings.BASE_URL + reverse('login') 
    message += 'Login here: ' + login_url

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email],
    )
    email.send()
"""