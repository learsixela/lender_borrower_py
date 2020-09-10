from django.db import models
from login.models import User
# Create your models here.

class PrestamoManager(models.Manager):
    def validar_registro(self, postData):
        errores = {}
        if int(postData['monto_prestamo']) < 1:
            errores['monto_prestamo'] = "Mlonto prestamo no puede ser inferior a 1"
        return errores

class Prestamo(models.Model):
    lender = models.ForeignKey(
        User, related_name="lender", on_delete=models.CASCADE)
    borrower = models.ManyToManyField(User, related_name="prestamos")
    monto_prestamo = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PrestamoManager()