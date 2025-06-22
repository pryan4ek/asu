# leader_portal/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone

from main.models import Club, Application
from student_portal.models import Subscription
from .models import Material
from .forms import LeaderClubForm, MaterialForm


def leader_required(view):
    return login_required(user_passes_test(lambda u: u.is_active and u.role == 'leader')(view))


@leader_required
def dashboard(request):
    # берем кружки, которыми управляет текущий руководитель
    clubs = request.user.managed_clubs.all()
    return render(request, "leader_portal/dashboard.html", {
        "clubs": clubs,
        "year": timezone.now().year
    })


@leader_required
def edit_club(request, pk):
    club = get_object_or_404(Club, pk=pk, manager=request.user)
    if request.method == "POST":
        form = LeaderClubForm(request.POST, request.FILES, instance=club)
        if form.is_valid():
            form.save()
            return redirect("leader_portal:dashboard")
    else:
        form = LeaderClubForm(instance=club)
    return render(request, "leader_portal/edit_club.html", {
        "form": form, "club": club, "year": timezone.now().year
    })


@leader_required
def participants(request, pk):
    club = get_object_or_404(Club, pk=pk, manager=request.user)
    subs = Subscription.objects.filter(club=club, status='active')
    return render(request, "leader_portal/participants.html", {
        "club": club, "subscriptions": subs, "year": timezone.now().year
    })


@leader_required
def manage_applications(request, pk):
    club = get_object_or_404(Club, pk=pk, manager=request.user)
    apps = Application.objects.filter(club=club, status='pending')
    if request.method == "POST":
        act = request.POST.get("action")
        app_id = request.POST.get("app_id")
        app = get_object_or_404(Application, pk=app_id, club=club)
        if act == "approve":
            app.status = "approved"
            app.moderated_at = timezone.now()
            app.save()
        elif act == "reject":
            app.status = "rejected"
            app.moderated_at = timezone.now()
            app.save()
        return redirect("leader_portal:manage_applications", pk=club.pk)
    return render(request, "leader_portal/manage_applications.html", {
        "club": club, "applications": apps, "year": timezone.now().year
    })


@leader_required
def materials(request, pk):
    club = get_object_or_404(Club, pk=pk, manager=request.user)
    mats = club.materials.all()
    if request.method == "POST":
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            mat = form.save(commit=False)
            mat.club = club
            mat.save()
            return redirect("leader_portal:materials", pk=club.pk)
    else:
        form = MaterialForm()
    return render(request, "leader_portal/materials.html", {
        "club": club, "materials": mats, "form": form, "year": timezone.now().year
    })
