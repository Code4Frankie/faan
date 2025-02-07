from django.db import models
from hod.models import Terminal
from hod.models import Unit
from hod.models import User

class LoggedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    terminal = models.ForeignKey(Terminal, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    equipment = models.CharField(max_length=100)
    fault = models.TextField()
    rectification = models.TextField()
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.user.first_name} - {self.date}"
