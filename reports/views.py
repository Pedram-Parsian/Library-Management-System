from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView

from circulation.models import Issue, Reserve, Renew
from users.models import Member


class DocumentReport(DetailView):
    ...


class DocumentsReport(ListView):
    ...


class MemberCard(DetailView):
    ...


class MemberReport(DetailView):
    ...


class MembersReport(ListView):
    ...


class MembersCards(ListView):
    ...


class IssueReceiptReport(DetailView):
    ...


class IssuesReport(ListView):
    ...


class RenewReceiptReport(DetailView):
    ...


class RenewsReport(ListView):
    ...


class ReserveReceiptReport(DetailView):
    ...


class ReservesReport(ListView):
    ...
