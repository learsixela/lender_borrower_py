from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Prestamo
from login.models import User
# Create your views here.

def home(request):

    reg_user = User.objects.get(id=request.session['user_id'])

    mis_registros = Prestamo.objects.filter(lender=User.objects.get(
        id=request.session['user_id']))

    prestamos= Prestamo.objects.all()
    lent_money=[]
    users_ids = []
    for prestamo in mis_registros:
        for borr in prestamo.borrower.all():
            lent_money.append({
                "lender":prestamo,
                "borrow":borr
            })
            users_ids.append(borr.id)

    borrower_list = []
    for usuario in User.objects.all():
        if int(usuario.rol) == 2 and (usuario.id not in users_ids):
            borrower_list.append(usuario)

    if reg_user.rol == 1:
        context = {
            "active_user": reg_user,
            "borrowers": borrower_list,
            "mi_borrower" : lent_money,
        }
        return render(request, 'lender.html', context)
    elif reg_user.rol == 2:

        prestamistas = []

        for prestamo in prestamos:
            for borr in prestamo.borrower.all():
                if reg_user.id == borr.id:
                    prestamistas.append({
                        "lender": prestamo,
                        "borrow": borr
                    })

        context = {
            "active_user": reg_user,
            "registros": prestamos,
            "prestamistas": prestamistas
        }
        return render(request, 'borrower.html', context)

def lend (request):
    prestamo = int(request.POST['prestamo'])
    lender = User.objects.get(id=request.session['user_id'])

    if(lender.money > prestamo and prestamo > 0) :
        lender.money = lender.money-prestamo
        lender.save()

        borrow = User.objects.get(id=request.POST['borrower'])
        suma_prestamo = prestamo + borrow.money
        borrow.money = suma_prestamo
        borrow.save()

        reg = Prestamo.objects.create(
            monto_prestamo=request.POST['prestamo'],
            lender= lender,
        )

        reg.borrower.add(borrow)
        reg.save()


    return redirect('/prestamos')