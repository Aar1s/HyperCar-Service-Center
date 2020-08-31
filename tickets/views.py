from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
import datetime
class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'welcome/index.html')


class MenuView(View):
    menu = {
        "Change oil": "change_oil",
        "Inflate tires": "tires",
        "Get diagnostic test": "diag"
    }

    def get(self, request, *args, **kwargs):
        return render(request, 'menu/menue.html', context={'menue': self.menu})


ticket_n = 0
waiting_time = 0

class TicketView(View):

    services = {
        "Change oil": 2,
        "Inflate tires": 5,
        "Get diagnostic test": 30,
    }
    def get(self, request, *args, **kwargs):
        global ticket_n, waiting_time
        ticket_n += 1
        waiting_time += 2
        return render(request, 'get_ticket/ticket.html', context={'ticket_number': ticket_n, 'waiting_time': waiting_time})
