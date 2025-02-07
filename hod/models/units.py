from django.db import models
from .terminals import Terminal
from .add_users import User

class Unit(models.Model):
    name = models.CharField(max_length=100)
    terminal = models.ForeignKey(Terminal, on_delete=models.CASCADE)
    unit_head = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


