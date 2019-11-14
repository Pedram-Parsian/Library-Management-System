from django.conf import settings
from django.db import models

from users.models import Member


class Bill(models.Model):
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} containing {self.billitem_set.count()} items'


class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    title = models.CharField(max_length=settings.CHARFIELD_MAX_LENGTH)
    description = models.TextField(max_length=settings.TEXTFIELD_MAX_LENGTH)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.price} - {self.title} for {self.bill}'


class Payment(models.Model):
    CASH = 10
    CREDIT = 20
    BALANCE = 30

    PAYMENT_CHOICES = (
        (CASH, 'Cash'),
        (CREDIT, 'Credit Card'),
        (BALANCE, 'Balance'),
    )

    # user = models.ForeignKey()
    payment_type = models.IntegerField(choices=PAYMENT_CHOICES)
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.amount} Rial on {self.timestamp}'
