from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class SuperAdmin(models.Model):
    first_name = models.CharField(max_length=50, default="FAAN")
    last_name = models.CharField(max_length=50, default="Admin")
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    
    def save(self, *args, **kwargs):
    # Hash the password before saving, only if it's not hashed
        if not check_password(self.password, make_password(self.password)):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


    @staticmethod
    def authenticate(email, password):
        try:
            super_admin = SuperAdmin.objects.get(email=email)
            if check_password(password, super_admin.password):
                return super_admin
            else:
                return None
        except SuperAdmin.DoesNotExist:
            return None
