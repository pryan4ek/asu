# main/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView
)
from django.urls import reverse_lazy
from django.db.models import Count, Q

from .models import Category, Club, Application, News
from .forms import ContactForm, ClubForm, CategoryForm, NewsForm, ApplicationForm


# --- Public views ---

def index(request):
    clubs = Club.objects.all()[:6]
    latest_news = News.objects.filter(is_approved=True).order_by("-published_at")[:5]
    return render(request, "index.html", {
        "clubs": clubs,
        "latest_news": latest_news,
        "year": timezone.now().year,
    })


def clubs(request):
    all_clubs = Club.objects.all()
    return render(request, "clubs.html", {
        "clubs": all_clubs,
        "year": timezone.now().year,
    })


def club_detail(request, slug):
    club = get_object_or_404(Club, slug=slug)
    applied = False

    # Проверяем, отправлял ли уже заявку текущий пользователь
    if request.user.is_authenticated:
        applied = Application.objects.filter(
            club=club,
            email=request.user.email
        ).exists()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(f"{reverse('login')}?next={request.path}")
        if not applied:
            # Создаём заявку от имени пользователя
            Application.objects.create(
                club=club,
                name=request.user.get_full_name() or request.user.username,
                email=request.user.email,
                status="pending",  # или сразу "approved", если не нужно модерации
                submitted_at=timezone.now()
            )
            applied = True

    return render(request, "club_detail.html", {
        "club": club,
        "applied": applied,
        "year": timezone.now().year,
    })


def news_list(request):
    posts = News.objects.filter(is_approved=True).order_by("-published_at")
    return render(request, "news_app/news_list.html", {
        "news_list": posts,
        "year": timezone.now().year,
    })


def news_detail(request, slug):
    post = get_object_or_404(News, slug=slug, is_approved=True)
    return render(request, "news_app/news_detail.html", {
        "news": post,
        "year": timezone.now().year,
    })


def contact(request):
    success = False
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # здесь логика отправки/сохранения
            success = True
            form = ContactForm()
    else:
        form = ContactForm()
    return render(request, "contact.html", {
        "form": form,
        "success": success,
        "year": timezone.now().year,
    })


def search(request):
    q = request.GET.get("q", "").strip()
    clubs_q = Club.objects.filter(
        Q(name__icontains=q) | Q(short_description__icontains=q)
    ) if q else Club.objects.none()
    news_q = News.objects.filter(
        Q(title__icontains=q) | Q(content__icontains=q),
        is_approved=True
    ) if q else News.objects.none()
    return render(request, "search_results.html", {
        "q": q,
        "clubs": clubs_q,
        "news": news_q,
        "year": timezone.now().year,
    })


# --- Dashboard (staff only) ---

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_active and self.request.user.is_staff

    def handle_no_permission(self):
        return redirect("index")


class DashboardHomeView(StaffRequiredMixin, DetailView):
    template_name = "dashboard/home.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"year": timezone.now().year})


# Category CRUD
class CategoryListView(StaffRequiredMixin, ListView):
    model = Category
    template_name = "dashboard/category_list.html"
    context_object_name = "categories"


class CategoryCreateView(StaffRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "dashboard/category_form.html"
    success_url = reverse_lazy("dashboard_category_list")


class CategoryUpdateView(StaffRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "dashboard/category_form.html"
    success_url = reverse_lazy("dashboard_category_list")


class CategoryDeleteView(StaffRequiredMixin, DeleteView):
    model = Category
    template_name = "dashboard/category_confirm_delete.html"
    success_url = reverse_lazy("dashboard_category_list")


# Club CRUD
class ClubListView(StaffRequiredMixin, ListView):
    model = Club
    template_name = "dashboard/club_list.html"
    context_object_name = "clubs"


class ClubCreateView(StaffRequiredMixin, CreateView):
    model = Club
    form_class = ClubForm
    template_name = "dashboard/club_form.html"
    success_url = reverse_lazy("dashboard_club_list")


class ClubUpdateView(StaffRequiredMixin, UpdateView):
    model = Club
    form_class = ClubForm
    template_name = "dashboard/club_form.html"
    success_url = reverse_lazy("dashboard_club_list")


class ClubDeleteView(StaffRequiredMixin, DeleteView):
    model = Club
    template_name = "dashboard/club_confirm_delete.html"
    success_url = reverse_lazy("dashboard_club_list")


# Application moderation
class ApplicationListView(StaffRequiredMixin, ListView):
    model = Application
    template_name = "dashboard/application_list.html"
    context_object_name = "applications"


class ApplicationDetailView(StaffRequiredMixin, DetailView):
    model = Application
    template_name = "dashboard/application_detail.html"
    context_object_name = "application"


def approve_application(request, pk):
    if not (request.user.is_active and request.user.is_staff):
        return redirect("index")
    app = get_object_or_404(Application, pk=pk)
    app.status = "approved"
    app.moderated_at = timezone.now()
    app.save()
    return redirect("dashboard_application_list")


def reject_application(request, pk):
    if not (request.user.is_active and request.user.is_staff):
        return redirect("index")
    app = get_object_or_404(Application, pk=pk)
    app.status = "rejected"
    app.moderated_at = timezone.now()
    app.save()
    return redirect("dashboard_application_list")


# News moderation
class NewsListView(StaffRequiredMixin, ListView):
    model = News
    template_name = "dashboard/news_list.html"
    context_object_name = "news_items"


def approve_news(request, pk):
    if not (request.user.is_active and request.user.is_staff):
        return redirect("index")
    item = get_object_or_404(News, pk=pk)
    item.is_approved = True
    item.published_at = timezone.now()
    item.save()
    return redirect("dashboard_news_list")


def unapprove_news(request, pk):
    if not (request.user.is_active and request.user.is_staff):
        return redirect("index")
    item = get_object_or_404(News, pk=pk)
    item.is_approved = False
    item.save()
    return redirect("dashboard_news_list")


# Statistics
def dashboard_stats(request):
    if not (request.user.is_active and request.user.is_staff):
        return redirect("index")
    clubs_stats = Club.objects.annotate(
        participants=Count("applications", filter=Q(applications__status="approved"))
    )
    categories_stats = Category.objects.annotate(
        club_count=Count("clubs")
    )
    total_applications = Application.objects.count()
    total_news = News.objects.count()
    return render(request, "dashboard/stats.html", {
        "clubs_stats": clubs_stats,
        "categories_stats": categories_stats,
        "total_applications": total_applications,
        "total_news": total_news,
        "year": timezone.now().year,
    })
