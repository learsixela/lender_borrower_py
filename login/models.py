from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errores = {}
        if len(User.objects.filter(email=postData['email'])) > 0:
            errores['existe'] = "Email ya registrado"
        else:
            if len(postData['nombre']) == 0:
                errores['nombre'] = "Firts Name  es obligatorio"
            if len(postData['apellido']) == 0:
                errores['apellido'] = "Last Name es obligatorio"
            EMAIL = re.compile(
                r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            if not EMAIL.match(postData['email']):
                errores['email'] = "email invalido"
            if len(postData['password']) < 6:
                errores['password'] = "Password debe ser mayor a 6 caracteres"
            if postData['password'] != postData['password2']:
                errores['password'] = "Password no son iguales"

            if postData['rol'] == '1':
                if int(postData['money']) < 1:
                    errores['money'] = "Un prestamista no puede ingresar sin dinero"
            elif postData['rol'] == '2':
                if len(postData['need_for']) < 6:
                    errores['need_for'] = "Need money for debe ser mayor a 6 caracteres"
                if len(postData['desc_for']) < 10:
                    errores['desc_for'] = "Description debe ser mayor a 10 caracteres"
                if int(postData['money_need']) < 1:
                    errores['money_need'] = "Amount Needed no puede ser menor a $1"
            else:
                errores['rol'] = "No existe perfil ingresado"
        return errores

    def encriptar(self, password):
        password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return password

    def validar_login(self, postData, usuario ):
        errores = {}
        if len(usuario) > 0:
            pw_given = postData['password']
            pw_hash = usuario[0].password

            if bcrypt.checkpw(pw_given.encode(), pw_hash.encode()) is False:
                errores['pass_incorrecto'] = "password es incorrecto"
        else:
            errores['usuario_invalido'] = "Usuario no existe"
        return errores

class User(models.Model):
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=255)
    rol = models.PositiveIntegerField(default=1)#render 1 , borrower 2
    money = models.PositiveIntegerField(default=1)
    need_for = models.CharField(max_length=40)
    desc_for = models.CharField(max_length=80)
    money_need= models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()