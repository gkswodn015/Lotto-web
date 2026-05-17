# lottery/admin.py

from django.contrib import admin
from .models import Round, Ticket, WinResult, Prize

admin.site.register(Round)
admin.site.register(Ticket)
admin.site.register(WinResult)
admin.site.register(Prize)
