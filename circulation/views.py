from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView
from bootstrap_modal_forms.generic import BSModalCreateView

from . import models
from users.models import Member
from . import forms


class ReserveView(LoginRequiredMixin, BSModalCreateView):
    object: models.Reserve
    template_name = 'circulation/reserve_modal.html'
    form_class = forms.ReserveForm
    success_message = 'The document was successfully reserved.'
    success_url = reverse_lazy('users:reserves')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.document_id = self.kwargs.get('id')
        self.object.member = Member.objects.get(user=self.request.user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'reserve'
        return context
