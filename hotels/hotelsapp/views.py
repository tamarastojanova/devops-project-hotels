from django.shortcuts import render, redirect
from .models import Room
from .forms import ReservationForm

def index(request):
    rooms = Room.objects.filter(is_clean=True, num_beds__lt=5)
    return render(request, "index.html", {"rooms": rooms})

def contactus(request):
    if request.method == "POST":
        form = ReservationForm(request.POST, files=request.FILES)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.image = form.cleaned_data['image']
            reservation.user = request.user
            reservation.save()
            return redirect('/index')

    else:
        form = ReservationForm()

    return render(request, "contactus.html", {"form": form})
