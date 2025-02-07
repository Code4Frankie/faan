# models/department.py
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    hod = models.OneToOneField('HOD', on_delete=models.SET_NULL, null=True, blank=True, related_name='department_hod')
    num_units = models.IntegerField(default=0)
    num_terminals = models.IntegerField(default=0)
    terminal_heads = models.CharField(max_length=100, null=True, blank=True)
    unit_heads = models.CharField(max_length=100, null=True, blank=True)

