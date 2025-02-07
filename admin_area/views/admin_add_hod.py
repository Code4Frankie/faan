from django.shortcuts import render, redirect
from django.contrib import messages
from admin_area.models import HOD, Department
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.hashers import make_password



def add_hod(request):
    if 'super_admin_id' in request.session:
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            department_id = request.POST.get('department')

            department = Department.objects.get(id=department_id)
            
            # Check if the department already has an HOD
            if department.hod:
                # Replace existing HOD with the new one
                department.hod.delete()

            # Hash the password
            hashed_password = make_password(password)

            # Create the new HOD
            new_hod = HOD.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=hashed_password,
                department=department
            )

            # Set the department's HOD to the new HOD
            department.hod = new_hod
            department.save()

            # Send email to the new HOD
            # send_hod_email(new_hod)

            messages.success(request, 'HOD added successfully.')
            return redirect('admin_dashboard')
        else:
            departments = Department.objects.all()
            return render(request, 'add_hod.html', {'departments': departments})
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')

"""
def send_hod_email(hod):
    subject = 'You are now the HOD of ' + hod.department.name
    message = 'Dear ' + hod.first_name + ',\n\nYou have been appointed as the Head of Department for ' + hod.department.name + '.\n\nPlease use the following credentials to login:\n\nEmail: ' + hod.email + '\nPassword: ' + hod.password + '\n\nAfter logging in, you will be asked to change your password.\n\nBest regards,\nFAAN\n\n'
    
    # Add login page link
    login_url = settings.BASE_URL + reverse('login') 
    message += 'Login here: ' + login_url

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[hod.email],
    )
    email.send()

"""