from django.shortcuts import render, redirect, get_object_or_404

from .forms import TrackerForm
from .models import Tracker
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
"""

def homess(request):
        month=request.GET.get('month')
        tracks=[]
        balance=0
        total_income = 0
        total_expense=0
        if month:
            months=int(month)
            tracks = Tracker.objects.filter(date__month=months)
            income=tracks.filter(type='Income')
            expense=tracks.filter(type='Expense')
            for i in income:
                total_income = total_income +i.amount
            for i in expense:
                total_expense=total_expense+i.amount
            balance=total_income-total_expense
        context = {
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': balance,
            'tracks':tracks,
        }

        return render(request, 'home.html', context)
"""

def logout(request):
    auth.logout(request)
    return redirect('login')
def register(request):
    if request.method=='POST':
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        user_name=request.POST.get('username')
        password_1=request.POST.get('password1')
        password_2=request.POST.get('password2')
        email = request.POST.get('email')
        if password_1==password_2:
            if User.objects.filter(username=user_name).exists():
                messages.info(request,'username already exists')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email already exists')
                return redirect('register')
            else:
                user=User.objects.create_user(username=user_name, first_name=first_name ,last_name=last_name ,password=password_1, email=email)
                user.save()
                print('user created')
                return redirect('login')

        else:
                messages.info(request,'passwords doesnt match')
                return redirect('register')

    else:
        return render(request,'register.html')

def login(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')
@login_required
def home(request):
    monthyear = request.GET.get('monthyear')
    tracks = []
    balance = 0
    total_income = 0
    total_expense = 0
    if monthyear:
        year,month=monthyear.split('-')
        tracks = Tracker.objects.filter(date__month=month,date__year=year,user=request.user)
        income = tracks.filter(type='Income')
        expense = tracks.filter(type='Expense')
        for i in income:
            total_income = total_income + i.amount
        for i in expense:
            total_expense = total_expense + i.amount
        balance = total_income - total_expense
    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'tracks': tracks,
    }

    return render(request, 'home.html', context)
@login_required
def add(request):
    if request.method=="POST":
        form=TrackerForm(request.POST)
        if form.is_valid():
            track=form.save(commit=False)
            track.user=request.user
            track.save()
            # Get the month and year from the track's date
            monthyear = track.date.strftime("%Y-%m")  # e.g. "2025-06"
            return redirect(f"/?monthyear={monthyear}")  # Redirect with selected month
            #return redirect('home')
    else:
        form=TrackerForm()
    return render(request,'add.html',{'form':form})
@login_required
def update(request,id):
    tracks=get_object_or_404(Tracker,id=id)
    if request.method=="POST":
        form=TrackerForm(request.POST,instance=tracks)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TrackerForm(instance=tracks)
    return render(request, 'update.html', {'form': form, 'tracks': tracks})
@login_required
def delete(request,id):
    tracks=get_object_or_404(Tracker,id=id)
    tracks.delete()
    return redirect('home')


