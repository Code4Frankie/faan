from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from hod.models import User, Terminal, Unit
from ..models import LoggedJob
import calendar

def unit_report(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        
        # Assuming unit_id is passed as a query parameter in the URL
        unit_id = request.GET.get('unit_id')
        
        if not unit_id:
            messages.error(request, 'Unit ID is required.')
            return redirect('dashboard')  
        
        try:
            unit = Unit.objects.get(id=unit_id)
        except Unit.DoesNotExist:
            messages.error(request, 'Unit matching the query does not exist.')
            return redirect('dashboard')  

        # Get the search query
        search_query = request.GET.get('search', '')
        logged_jobs = LoggedJob.objects.filter(unit=unit)

        if search_query:
            # Convert the month name to a number
            try:
                month_number = list(calendar.month_name).index(search_query)
                if month_number == 0:  # if month is not found
                    raise ValueError
            except ValueError:
                messages.error(request, 'Invalid month name.')
                return redirect('unit_report', unit_id=unit_id)

            # Filter jobs by the selected month
            logged_jobs = logged_jobs.filter(date__month=month_number)

        # Paginate the job logs
        paginator = Paginator(logged_jobs, 20)  # Show 20 jobs per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'unit': unit,
            'page_obj': page_obj,
            'search_query': search_query,
        }

        return render(request, 'unit_report.html', context)
    else:
        messages.error(request, 'Please login to access this page')
        return redirect('login')
