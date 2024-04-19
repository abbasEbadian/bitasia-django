from django.contrib import admin

from ticket.models import Ticket, TicketMessage

admin.site.register(Ticket)
admin.site.register(TicketMessage)
