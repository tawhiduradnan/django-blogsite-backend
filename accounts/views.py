
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.forms import RegistrationForm


# Step 1: User Registration
class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')  # Redirect to login page after successful registration


# Step 2: User Dashboard
# @login_required
# def dashboard_view(request):
#     return render(request, 'registration/dashboard.html')