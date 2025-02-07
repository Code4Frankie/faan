# unit_head_unit_report.py
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.worksheet.protection import SheetProtection
from django.contrib import messages
from hod.models import User, Unit
from ..models import LoggedJob
import calendar

def unit_head_unit_report(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        
        # Check if the user is a unit head
        if user.unit_head:
            # Fetch the unit headed by this user
            unit = Unit.objects.filter(unit_head=user).first()
            if unit:
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
                        return redirect('unit_head_unit_report')

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
                return render(request, 'unit_head_unit_report.html', context)
            else:
                messages.error(request, 'You are not assigned as the head of any unit.')
                return redirect('login')
        else:
            messages.error(request, 'You do not have the required permissions.')
            return redirect('login')
    else:
        messages.error(request, 'Please log in to access')
        return redirect('login')

def download_unit_head_report(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)

        # Check if the user is a unit head
        if user.unit_head:
            # Fetch the unit headed by this user
            unit = Unit.objects.filter(unit_head=user).first()
            if unit:
                # Create a new workbook
                wb = Workbook()
                ws = wb.active

                # Define headers
                headers = [
                    'User Name', 'Email', 'Date of Fault', 'Place of Fault', 
                    'Equipment', 'Fault', 'Rectification', 'Status'
                ]
                ws.append(headers)

                # Add data to the worksheet
                for report in unit.loggedjob_set.all():
                    # Convert datetime to naive datetime (without timezone information)
                    date_added = report.date.replace(tzinfo=None) if report.date else None
                    
                    ws.append([
                        f"{report.user.first_name} {report.user.last_name}",
                        report.user.email,
                        date_added,
                        report.location,
                        report.equipment,
                        report.fault,
                        report.rectification,
                        report.status
                    ])
                
                # Protect the worksheet
                ws.protection.sheet = True
                ws.protection.password = 'password'  # Set a password for the protection, can be any string

                # Save the workbook
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename={unit.name}_report.xlsx'
                wb.save(response)
                return response
            else:
                messages.error(request, 'You are not assigned as the head of any unit.')
                return redirect('login')
        else:
            messages.error(request, 'You do not have the required permissions.')
            return redirect('login')
    else:
        messages.error(request, 'Please log in to access')
        return redirect('login')
