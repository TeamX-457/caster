from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import WaitlistSignupForm


class HomeView(FormView):
    template_name = 'marketing/home.html'
    form_class = WaitlistSignupForm
    success_url = reverse_lazy('marketing:home')

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            "You're on the list! We'll be in touch with early access details.",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below and try again.')
        return super().form_invalid(form)
