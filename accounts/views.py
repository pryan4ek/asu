# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout

from .forms import StudentSignUpForm


def register(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = StudentSignUpForm()
    return render(request, 'accounts/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('student_portal:dashboard')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('index')


# Декораторы по ролям
def role_required(role):
    def decorator(view_func):
        return login_required(user_passes_test(lambda u: u.role == role)(view_func))

    return decorator


leader_required = role_required('leader')
admin_required = role_required('admin')


def logout_view(request):
    logout(request)
    return redirect('index')
