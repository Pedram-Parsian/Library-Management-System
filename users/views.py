from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic import View, TemplateView, DetailView
from django.views.generic.edit import (
    FormView,
    DeleteView,
    FormMixin)
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.conf import settings
from django.http import HttpResponse

from circulation.models import Reserve, Issue
from documents.models import Review
from ticketing.models import Ticket, Reply, Attachment
from ticketing.forms import TicketForm, ReplyForm
from . import forms
from . import models


class SignupView(FormView):
    template_name = "users/signup.html"
    form_class = forms.CustomUserCreationForm

    def get_success_url(self):
        return reverse_lazy('signup_complete')

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()
        messages.info(self.request, "You signed up successfully.")
        return response


class UserLogoutView(LogoutView):
    template_name = "users/logout.html"

    def get_success_url(self):
        redirect_to = self.request.POST.get("next", "/")
        return redirect_to


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = forms.LoginForm
    redirect_authenticated_user = True


class ProfileView(LoginRequiredMixin, FormView):
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Your Information has been Updated.')
        return super(ProfileView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = 'profile'
        return context

    def get_form_kwargs(self):
        kwargs = super(ProfileView, self).get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    success_url = reverse_lazy('users:profile')
    form_class = forms.UpdateInfo
    login_url = reverse_lazy('users:login')
    template_name = 'users/profile/profile.html'


class ProfileReviewsView(LoginRequiredMixin, ListView):
    model = Review
    login_url = reverse_lazy('users:login')
    template_name = 'users/profile/reviews.html'

    def get_queryset(self):
        return Review.objects.filter(member=self.request.user.member).order_by('-date_added')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = 'reviews'
        return context


class ProfileTicketsView(LoginRequiredMixin, ListView):
    model = Ticket
    login_url = reverse_lazy('users:login')
    template_name = 'users/profile/tickets.html'

    def get_queryset(self):
        return Ticket.objects.filter(member=self.request.user.member).order_by('-date_opened')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = 'tickets'
        return context


class ProfileCreateTicketView(FormView):
    object: Ticket
    template_name = 'users/profile/create_ticket.html'
    form_class = TicketForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = 'tickets'
        context['MAX_FILES_COUNT'] = settings.MAX_ATTACHMENTS
        import humanize
        context['MAX_FILE_SIZE'] = humanize.naturalsize(settings.MAX_ATTACHMENT_SIZE, format='%.0f')
        return context

    def get_success_url(self):
        return reverse_lazy('users:ticket_detail', kwargs={'pk': self.object.id})

    def get_form_kwargs(self):
        # passing request to form so that we can validate the total uploaded files count.
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.member = self.request.user.member
        self.object.status = Ticket.OPEN
        self.object.save()

        # Now that we have the Ticket object saved,
        # we can create and save a reply object:
        reply = Reply(ticket_id=self.object.id)
        reply.user_id = self.request.user.id
        reply.text = form.cleaned_data.get('text')
        reply.save()

        # then we can save attachments
        for i, file in enumerate(self.request.FILES.getlist('attachments')):
            attachment = Attachment(reply=reply)
            attachment.file = file
            attachment.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Something went wrong! Please correct the form and re-submit it.')
        return super().form_invalid(form)


# todo Is there any better solution for submitting form inside DetailView?
# https://docs.djangoproject.com/en/2.2/topics/class-based-views/mixins/#an-alternative-better-solution
class ProfileTicketView(LoginRequiredMixin, FormMixin, DetailView):
    object: Reply
    template_name = 'users/profile/ticket_detail.html'
    model = Ticket
    form_class = ReplyForm

    def get_success_url(self):
        return reverse_lazy('users:ticket_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replies'] = Reply.objects.filter(ticket_id=self.object.pk)
        context['sidebar'] = 'tickets'
        context['MAX_FILES_COUNT'] = settings.MAX_ATTACHMENTS
        import humanize
        context['MAX_FILE_SIZE'] = humanize.naturalsize(settings.MAX_ATTACHMENT_SIZE, format='%.0f')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form_kwargs(self):
        # passing request to form so that we can validate the total uploaded files count.
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        # first, we complete and save the reply object
        form.instance.ticket = self.get_object()
        form.instance.user = self.request.user
        reply = form.save()

        # now we can save attachments
        for i, file in enumerate(self.request.FILES.getlist('attachments')):
            attachment = Attachment(reply=reply)
            attachment.file = file
            attachment.save()

        messages.success(self.request, "Your reply has been submitted. Thanks!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Something went wrong! Please correct the form and re-submit it.')
        return super().form_invalid(form)


class ProfileReservesView(LoginRequiredMixin, ListView):
    model = Reserve
    login_url = reverse_lazy('users:login')
    template_name = 'users/profile/reserves.html'

    def get_queryset(self):
        # todo maybe finding a more efficient way for finding the corresponding member:
        return Reserve.objects.filter(member__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = 'reserves'
        return context


class ProfileIssuesView(LoginRequiredMixin, ListView):
    model = Issue
    login_url = reverse_lazy('users:login')
    template_name = 'users/profile/issues.html'

    def get_queryset(self):
        # todo maybe finding a more efficient way for finding the corresponding member:
        return Issue.objects.filter(member__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = 'issues'
        return context


class ProfileReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    success_url = reverse_lazy("users:reviews")

    # todo oh... is it the right way?! or shall we send a post request?
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ProfileReserveDelete(LoginRequiredMixin, DeleteView):
    model = Reserve
    success_url = reverse_lazy("users:reserves")

    # todo oh... is it the right way?! or shall we send a post request?
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class SignupCompleteView(TemplateView):
    template_name = 'users/signup_complete.html'


class AccountEmailActivationView(View):
    def get(self, request, key):
        context = {}
        qs = models.EmailActivation.objects.filter(key__iexact=key)
        if qs.count() > 0:
            if qs.count() == 1:
                confirm_qs = qs.confirmable()
                if confirm_qs.count() == 1:
                    obj = confirm_qs.first()
                    obj.activate()
                    messages.success(self.request, f'Your email has been activated {obj.user.first_name.capitalize()}!'
                                                   f' You can now login.')
                    return redirect('login')
                else:
                    not_confirmable_object = qs.first()
                    if not_confirmable_object.is_activated:
                        messages.info(self.request, f'Oops! You have already activated your email'
                                                    f' {not_confirmable_object.user.first_name.capitalize()}!')
                        return redirect('login')
                    elif not_confirmable_object.forced_expired:
                        context['ERR_TYPE'] = 'FORCED_EXPIRED'
                        return render(request, 'users/email_activation/error.html', context)
                    else:
                        context['ERR_TYPE'] = 'EXPIRED'
                        context['EXPIRE_DAYS'] = settings.DEFAULT_ACTIVATION_DAYS
                        return render(request, 'users/email_activation/error.html', context)
            else:
                return HttpResponse(status=500)
        else:
            return render(request, 'users/email_activation/error.html', context)


class ResendActivationEmail(FormView):
    template_name = 'users/email_activation/resend.html'
    form_class = forms.ReactivateEmailForm
    success_url = reverse_lazy('users:resend_activation_email_successful')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        obj = models.EmailActivation.objects.email_exists(email).first()
        user = obj.user
        new_activation = models.EmailActivation.objects.create(user=user, email=email)
        new_activation.send_activation_email()
        return super(ResendActivationEmail, self).form_valid(form)


class ResendActivationEmailSuccessful(TemplateView):
    template_name = 'users/email_activation/resend_successful.html'
