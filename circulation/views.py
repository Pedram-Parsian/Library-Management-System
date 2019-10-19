from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView
from bootstrap_modal_forms.generic import BSModalCreateView

from . import forms, models


class ReserveView(BSModalCreateView):
    template_name = 'circulation/reserve_modal.html'
    form_class = forms.ReserveForm
    success_message = 'The document was successfully reserved.'
    # todo change the success_url to member's profile page -> reserves section or
    #  document detail page with reserved (disabled) button:
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'reserve'
        return context
