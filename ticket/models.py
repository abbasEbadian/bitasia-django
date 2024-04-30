from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

from exchange.models import BaseModel

User = get_user_model()


class Ticket(BaseModel):
    class Department(models.TextChoices):
        FINANCE = "finance", _("Finance")
        SUPPORT = "support", _("Support")
        ADMINISTRATION = "administration", _("Administration")

    class Status(models.TextChoices):
        ANSWERED = "answered", _("Answered")
        PENDING = "pending", _("Pending")
        CLOSED = ("closed", _("Closed"))

    user_id = models.ForeignKey(User, related_name='tickets', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    department = models.CharField(choices=Department.choices, default=Department.SUPPORT, max_length=24)
    status = models.CharField(choices=Status.choices, default=Status.PENDING, max_length=24)

    def __str__(self):
        return f"{self.title} | {self.user_id.username}"

    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')


class TicketMessage(BaseModel):
    ticket_id = models.ForeignKey(Ticket, related_name='messages', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, related_name='ticket_messages', on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return f"{self.message[:32]}"

    class Meta:
        verbose_name = _('Ticket Message')
        verbose_name_plural = _('Ticket Messages')
