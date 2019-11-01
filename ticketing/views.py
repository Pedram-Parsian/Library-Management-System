from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from bootstrap_modal_forms.generic import BSModalCreateView

from ticketing.models import Ticket, Reply
from . import forms
from . import models


class TicketCreateView(LoginRequiredMixin, BSModalCreateView):
    object: Ticket
    template_name = 'ticketing/create_ticket.html'
    form_class = forms.TicketCreateForm
    success_message = 'Your ticket was successfully submitted. Thanks!'

    def get_success_url(self):
        return reverse_lazy('users:ticket_detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.member = self.request.user.member
        self.object.status = models.Ticket.OPEN
        self.object.save()

        # Now that we have the Ticket object saved,
        # we can create and save a reply object:
        reply = Reply(ticket_id=self.object.id)
        reply.user_id = self.request.user.id
        reply.text = form.cleaned_data.get('text')
        reply.save()

        return super().form_valid(form)
