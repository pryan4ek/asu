from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from main.models import Club
from .models import Subscription, Review, Notification
from .forms import ReviewForm


@login_required
def dashboard(request):
    subs = Subscription.objects.filter(user=request.user, status='active')

    schedule = []
    for sub in subs:
        club = sub.club
        if club.schedule:
            schedule.append({
                'club': club,
                'text': club.schedule
            })

    reviews = {r.club_id: r for r in request.user.reviews.all()}

    return render(request, 'dashboard.html', {
        'subscriptions': subs,
        'schedule': schedule,
        'reviews': reviews,
        'year': timezone.now().year,
    })


@login_required
def unsubscribe(request, pk):
    sub = get_object_or_404(Subscription, pk=pk, user=request.user)
    sub.status = 'cancelled'
    sub.updated_at = timezone.now()
    sub.save()
    Notification.objects.create(
        user=request.user,
        message=f"Вы отписались от кружка «{sub.club.name}»",
        link=sub.club.get_absolute_url()
    )
    return redirect('student_portal:dashboard')


@login_required
def leave_review(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    if not Subscription.objects.filter(user=request.user, club=club, status='active').exists():
        return redirect('student_portal:dashboard')

    try:
        review = Review.objects.get(user=request.user, club=club)
    except Review.DoesNotExist:
        review = None

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            rev = form.save(commit=False)
            rev.user = request.user
            rev.club = club
            rev.created_at = timezone.now()
            rev.save()
            Notification.objects.create(
                user=request.user,
                message=f"Ваш отзыв о «{club.name}» сохранён"
            )
            return redirect('student_portal:dashboard')
    else:
        form = ReviewForm(instance=review)

    return render(request, 'leave_review.html', {
        'form': form,
        'club': club,
        'year': timezone.now().year,
    })


@login_required
def notifications(request):
    notes = request.user.notifications.all()
    notes.update(is_read=True)
    return render(request, 'notifications.html', {
        'notifications': notes,
        'year': timezone.now().year,
    })
