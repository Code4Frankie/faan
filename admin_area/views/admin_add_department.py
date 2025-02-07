# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import Department

def add_department(request):
    # Check if super_admin_id is present in session
    if 'super_admin_id' not in request.session:
        # If super admin is not logged in, redirect to login page or display an error message
        messages.error(request, 'You need to log in as super admin to add a department.')
        return redirect('login')

    if request.method == 'POST':
        # Get the form data from the request
        name = request.POST.get('title')
        
        # Create a new department instance
        department = Department.objects.create(name=name)
        
        # Optionally, you can assign other fields to the department instance here
        
        # Save the department instance
        department.save()
        
        # Optionally, you can add a success message
        messages.success(request, 'Department added successfully.')
        
        # Redirect to the admin dashboard or any other page
        return redirect('admin_dashboard')
    
    # If the request method is GET, render the add department form
    return render(request, 'admin_add_department.html')
