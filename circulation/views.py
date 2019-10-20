from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView
from bootstrap_modal_forms.generic import BSModalCreateView

from users.models import Member
from . import forms, models


class ReserveView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'circulation/reserve_modal.html'
    form_class = forms.ReserveForm
    success_message = 'The document was successfully reserved.'
    # todo change the success_url to member's profile page -> reserves section or
    #  document detail page with reserved (disabled) button:
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.member = Member.objects.get(user=self.request.user)
        self.object.document_id = self.kwargs.get('id')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'reserve'
        return context
