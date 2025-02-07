from django.shortcuts import render, get_object_or_404, redirect
from admin_area.models import HOD
from ..models import Terminal, Unit
from django.core.paginator import Paginator
from django.http import HttpResponse
from openpyxl import Workbook
from django.utils import timezone
from django.utils.dateparse import parse_date
from datetime import datetime
from django.http import JsonResponse
from django.template.loader import render_to_string


def view_terminal_report(request, terminal_id):
    if 'hod_id' in request.session:
        hod_id = request.session['hod_id']
        hod = HOD.objects.get(id=hod_id)

        # Fetch the terminal object
        terminal = get_object_or_404(Terminal, id=terminal_id)

        # Fetch all units in the terminal
        units = Unit.objects.filter(terminal=terminal)

        # Paginate the units
        paginator = Paginator(units, 2)  # Display 2 units per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'hod': hod,
            'terminal': terminal,
            'page_obj': page_obj,
            'units': units,
        }
        return render(request, 'hod_view_terminal_report.html', context)
    else:
        # Handle case where HOD is not logged in
        return redirect('login')


def ajax_search_reports(request):
    unit_id = request.GET.get('unit_id', '')
    search_query = request.GET.get('search', '')
    
    try:
        unit = Unit.objects.get(id=unit_id)
        reports = unit.loggedjob_set.all()

        if search_query:
            try:
                # Attempt to parse the month from the search query
                search_date = datetime.strptime(search_query, "%B")
                # Filter reports by the month
                reports = reports.filter(date__month=search_date.month)
            except ValueError:
                # If parsing fails, return no reports
                reports = reports.none()
        
        html = render_to_string('partials/_reports_list.html', {'unit': unit, 'reports': reports})
        return JsonResponse({'html': html})
    except Unit.DoesNotExist:
        return JsonResponse({'html': ''})



def download_unit_report(request, unit_id):
    # Retrieve the unit object
    unit = get_object_or_404(Unit, id=unit_id)
    
    # Create a new workbook
    wb = Workbook()
    ws = wb.active

    # Define headers
    headers = [
        'Terminal Name', 'Unit Name', 'User Name', 'Email', 
        'Date of fault', 'Place of fault', 'Equipment', 'Fault', 
        'Rectification', 'Status'
    ]
    ws.append(headers)

    # Add data to the worksheet
    for report in unit.loggedjob_set.all():
        # Convert datetime to naive datetime (without timezone information)
        date_added = report.date.replace(tzinfo=None) if report.date else None
        
        ws.append([
            report.terminal.name,
            unit.name,
            f"{report.user.first_name} {report.user.last_name}",
            report.user.email,
            date_added,
            report.location,
            report.equipment,
            report.fault,
            report.rectification,
            report.status
        ])

    # Save the workbook
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={unit.name}_report.xlsx'
    wb.save(response)
    return response
