from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import *
import bcrypt, datetime


# Create your views here.
def index(request):
    return redirect('/main')

def main(request):
    return render(request,'main.html')

def newAccount(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        confirm_pw = request.POST['confirm_pw']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        confirm_pw_hash = bcrypt.hashpw(confirm_pw.encode(), bcrypt.gensalt()).decode()
        registration = User.objects.create(name = request.POST['name'], username = request.POST['username'], password = pw_hash, confirm_pw = confirm_pw_hash)
        account = User.objects.filter(username = request.POST['username'])
        account = account[0]
        request.session['loggedInAccountID'] = account.id
        return redirect('/travels')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        account = User.objects.filter(username = request.POST['username'])
        account = account[0]
        request.session['loggedInAccountID'] = account.id
    return redirect("/travels")

def travels(request):
    if 'loggedInAccountID' not in request.session:
        return redirect('/')
    user = User.objects.get(id = request.session['loggedInAccountID'])
    joined = Trip.objects.filter(travelers = user)
    travel = Trip.objects.exclude(Q(creator = user) | Q(travelers = user))
    context = {
        'user' : user,
        'travel': travel,
        'joined' : joined,
    }
    return render(request, 'travels.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def addpage(request):
    if 'loggedInAccountID' not in request.session:
        return redirect('/')
    current = datetime.date.today()
    current = str(current)
    context = {
        'current' : current,
    }
    return render(request, 'add.html',context)

def newTrip(request):
    user = User.objects.get(id = request.session['loggedInAccountID'])
    errors = Trip.objects.Trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/travels/add')
    else:
        planTrip = Trip.objects.create(creator = user, destination = request.POST['destination'], desc = request.POST['desc'], date_from = request.POST['date_from'], date_to = request.POST['date_to'])
        return redirect('/travels')

def tripInfo(request, tripID):
    if 'loggedInAccountID' not in request.session:
        return redirect('/')
    trip = Trip.objects.get(id = tripID)
    context = {
        'trip' : trip,
    }
    return render(request, 'trip.html',context)

def joinPlan(request, planID):
    user = User.objects.get(id = request.session['loggedInAccountID'])
    plan = Trip.objects.get(id = planID)
    plan.travelers.add(user)
    return redirect('/travels')