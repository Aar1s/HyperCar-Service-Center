from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from collections import deque
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
        return render(request, 'menu/menu.html')


ticket_n = 0
waiting_time = 0
class TicketView(MenuView):
    line_of_cars = {'Oil': 0, 'Tires': 0, 'Diagnostics':0}

    def get(self, request, *args, **kwargs):
        global ticket_n, waiting_time

class OilView(TicketView):
    def get(self, request, *args, **kwargs):
        global ticket_n, waiting_time
        ticket_n += 1
        super().line_of_cars['Oil'] += 1
        if ticket_n <= 2:
            waiting_time = 0
        else:
            if super().line_of_cars['Oil'] == 2:
                waiting_time = 2 * super().line_of_cars['Oil'] - 2
            else:
                waiting_time = 2 * super().line_of_cars['Oil']
        return render(request, 'get_ticket/ticket.html', context=
        {
            'ticket_number': ticket_n,
            'waiting_time': waiting_time,
            'oil': super().line_of_cars['Oil'],
            'tires': super().line_of_cars['Tires'],
            'diagnostics': super().line_of_cars['Diagnostics']
        })


class TireView(TicketView):
    def get(self, request, *args, **kwargs):
        global ticket_n, waiting_time
        ticket_n += 1
        super().line_of_cars['Tires'] += 1
        if ticket_n <= 2:
            waiting_time = 0
        else:
            if super().line_of_cars['Tires'] == 2:
                waiting_time = 2 * super().line_of_cars['Tires'] + 5 * super().line_of_cars['Tires'] - 5
            else:
                waiting_time = 2 * super().line_of_cars['Tires'] + 5 * super().line_of_cars['Tires']

        return render(request, 'get_ticket/ticket.html', context=
        {
            'ticket_number': ticket_n,
            'waiting_time': waiting_time,
            'oil': super().line_of_cars['Oil'],
            'tires': super().line_of_cars['Tires'],
            'diagnostics': super().line_of_cars['Diagnostics']
        })


class DiagView(TicketView):
    def get(self, request, *args, **kwargs):
        global ticket_n, waiting_time
        ticket_n += 1
        super().line_of_cars['Diagnostics'] += 1
        if ticket_n <= 2:
            waiting_time = 0
        elif super().line_of_cars['Diagnostics'] == 1:
            waiting_time = 2 * super().line_of_cars['Tires'] + 5 * super().line_of_cars['Tires']
        else:
            if super().line_of_cars['Diagnostics'] == 2:
                waiting_time = 2 * super().line_of_cars['Diagnostics'] + 5 * super().line_of_cars['Diagnostics'] + 30 * super().line_of_cars['Diagnostics'] - 30
            else:
                waiting_time = 2 * super().line_of_cars['Diagnostics'] + 5 * super().line_of_cars['Diagnostics'] + 30 * super().line_of_cars['Diagnostics']

        return render(request, 'get_ticket/ticket.html', context=
        {
            'ticket_number': ticket_n,
            'waiting_time': waiting_time,
            'oil': super().line_of_cars['Oil'],
            'tires': super().line_of_cars['Tires'],
            'diagnostics': super().line_of_cars['Diagnostics']
        })


class OperatorView(TicketView):
    def get(self, request, *args, **kwargs):
        global ticket_n, waiting_time
        return render(request, 'processing/processing.html', context=
        {
            'oil': super().line_of_cars['Oil'],
            'tires': super().line_of_cars['Tires'],
            'diagnostics': super().line_of_cars['Diagnostics']
        })
