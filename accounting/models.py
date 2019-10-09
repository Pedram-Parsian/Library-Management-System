from django.db import models


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

    def __str__(self):
        return f'{self.amount} Rial on {self.timestamp}'
