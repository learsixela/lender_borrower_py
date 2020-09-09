from django.shortcuts import render, redirect
from django.contrib import messages
from time import gmtime, strftime
import bcrypt

from .models import User

# Create your views here.
def login(request):
    return render(request, 'login.html')
def registrar(request):
    return render(request, 'registro.html')

def inicio(request):
    usuario = User.objects.filter(email=request.POST['email'])
    errores = User.objects.validar_login(request.POST, usuario)

    if len(errores) > 0:
        for key, msg in errores.items():
            messages.error(request, msg)
        return redirect('/')
    else:
        request.session['user_id'] = usuario[0].id
        return redirect('/sistemas')

def registro(request):
    #validacion de parametros
    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, msg in errors.items():
            messages.error(request, msg)
        return redirect('/registrar')

    else:
        #encriptar password
        password = User.objects.encriptar(request.POST['password'])
        decode_hash_pw = password.decode('utf-8')
        #crear usuario
        if request.POST['rol'] == '1':
            user = User.objects.create(
                nombre=request.POST['nombre'],
                apellido=request.POST['apellido'],
                email=request.POST['email'],
                password=decode_hash_pw,
                rol=1,
                money=request.POST['money'],
                money_need=0,
            )
        else:
            user = User.objects.create(
                nombre=request.POST['nombre'],
                apellido=request.POST['apellido'],
                email=request.POST['email'],
                password=decode_hash_pw,
                rol=2,
                need_for = request.POST['need_for'],
                desc_for = request.POST['desc_for'],
                money_need = request.POST['money_need'],
                money=0,
            )
        request.session['user_id'] = user.id
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')