from django.urls import path
from .views import hod_dashboard, hod_profile, hod_logout, hod_add_users, hod_edit_users, hod_remove_users, hod_add_terminal, edit_terminal, edit_terminals, delete_terminal, add_units, view_terminal_reports, view_terminal_report, download_unit_report, edit_units, edit_unit, delete_unit, ajax_search_reports

urlpatterns = [
    path('hod_dashboard/', hod_dashboard, name='hod_dashboard'),  
    path('hod_profile/', hod_profile, name='hod_profile'),
    path('hod_logout/', hod_logout, name='hod_logout'),
    path('hod_add_users/', hod_add_users, name='hod_add_users'),
    path('hod_edit_users/', hod_edit_users, name='hod_edit_users'),
    path('hod_remove_users/', hod_remove_users, name='hod_remove_users'),
    path('hod_add_terminal/', hod_add_terminal, name='hod_add_terminal'),
    path('edit_terminal/<int:terminal_id>/', edit_terminal, name='edit_terminal'),
    path('delete_terminal/', delete_terminal, name='delete_terminal'),
    path('edit_terminals/', edit_terminals, name='edit_terminals'),
    path('add_units/', add_units, name='add_units'),
    path('view_terminal_reports', view_terminal_reports, name='view_terminal_reports'),
    path('ajax_search_reports/', ajax_search_reports, name='ajax_search_reports'),

    path('view_terminal_report/<int:terminal_id>/', view_terminal_report, name='view_terminal_report'),
    
    path('download_unit_report/<int:unit_id>/', download_unit_report, name='download_unit_report'),
    path('edit_units/', edit_units, name='edit_units'),
    path('edit_unit/<int:unit_id>/', edit_unit, name='edit_unit'),
    path('delete_unit/', delete_unit, name='delete_unit'),


]