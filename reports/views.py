from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView

from circulation.models import Issue, Reserve, Renew
from users.models import Member
from documents.models import Document


class DocumentReport(DetailView):
    template_name = 'reports/document.html'
    model = Document


class DocumentsReport(ListView):
    template_name = 'reports/documents.html'
    model = Document


class MemberCard(DetailView):
    # just return a pdf
    model = Member

    def get(self, request, *args, **kwargs):
        ...


class MemberReport(DetailView):
    template_name = 'reports/member.html'
    model = Member


class MembersReport(ListView):
    template_name = 'reports/members.html'
    model = Member


class MembersCards(ListView):
    # just return a pdf
    model = Member


class IssueReceiptReport(DetailView):
    # just return a pdf
    model = Issue


class IssuesReport(ListView):
    template_name = 'reports/issues.html'
    model = Issue


class RenewReceiptReport(DetailView):
    # just return a pdf
    model = Renew


class RenewsReport(ListView):
    template_name = 'reports/renews.html'
    model = Renew


class ReserveReceiptReport(DetailView):
    # just return a pdf
    model = Reserve


class ReservesReport(ListView):
    template_name = 'reports/reserves.html'
    model = Reserve
