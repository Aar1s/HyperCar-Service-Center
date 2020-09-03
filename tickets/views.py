from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
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
    line_of_cars = {'Oil': {'Quantity': 0, 'ticket_numbers': []},
                'Tires': {'Quantity': 0, 'ticket_numbers': []},
                'Diagnostics': {'Quantity': 0, 'ticket_numbers': []}}
    tickets = {}


class OilView(TicketView):
    def get(self, request, *args, **kwargs):
        global ticket_n, waiting_time
        ticket_n += 1
        super().line_of_cars['Oil']['Quantity'] += 1
        super().line_of_cars['Oil']['ticket_numbers'].append(ticket_n)
        if ticket_n <= 2:
            waiting_time = 0
        else:
            if super().line_of_cars['Oil']['Quantity'] == 2:
                waiting_time = 2 * super().line_of_cars['Oil']['Quantity'] - 2
            else:
                waiting_time = 2 * super().line_of_cars['Oil']['Quantity']
        return render(request, 'get_ticket/ticket.html', context={
            'ticket_number': ticket_n,
            'waiting_time': waiting_time,
            'oil': super().line_of_cars['Oil']['Quantity'],
            'tires': super().line_of_cars['Tires']['Quantity'],
            'diagnostics': super().line_of_cars['Diagnostics']['Quantity']
        })


class TireView(TicketView):
    def get(self, request, *args, **kwargs):
        global ticket_n, waiting_time
        ticket_n += 1
        super().line_of_cars['Tires']['Quantity'] += 1
        super().line_of_cars['Tires']['ticket_numbers'].append(ticket_n)
        if ticket_n <= 2:
            waiting_time = 0
        else:
            if super().line_of_cars['Tires']['Quantity'] == 2:
                waiting_time = 2 * super().line_of_cars['Tires']['Quantity'] +\
                               5 * super().line_of_cars['Tires']['Quantity'] - 5
            else:
                waiting_time = 2 * super().line_of_cars['Tires']['Quantity'] +\
                               5 * super().line_of_cars['Tires']['Quantity']

        return render(request, 'get_ticket/ticket.html', context={
            'ticket_number': ticket_n,
            'waiting_time': waiting_time,
            'oil': super().line_of_cars['Oil']['Quantity'],
            'tires': super().line_of_cars['Tires']['Quantity'],
            'diagnostics': super().line_of_cars['Diagnostics']['Quantity']
        })


class DiagView(TicketView):
    def get(self, request, *args, **kwargs):
        global ticket_n, waiting_time
        ticket_n += 1
        super().line_of_cars['Diagnostics']['Quantity'] += 1
        super().line_of_cars['Diagnostics']['ticket_numbers'].append(ticket_n)
        if ticket_n <= 2:
            waiting_time = 0
        elif super().line_of_cars['Diagnostics']['Quantity'] == 1:
            waiting_time = 2 * super().line_of_cars['Tires']['Quantity'] + 5 * super().line_of_cars['Tires']['Quantity']
        else:
            if super().line_of_cars['Diagnostics']['Quantity'] == 2:
                waiting_time = 2 * super().line_of_cars['Diagnostics']['Quantity'] +\
                               5 * super().line_of_cars['Diagnostics']['Quantity'] +\
                               30 * super().line_of_cars['Diagnostics']['Quantity'] - 30
            else:
                waiting_time = 2 * super().line_of_cars['Diagnostics']['Quantity'] +\
                               5 * super().line_of_cars['Diagnostics']['Quantity'] +\
                               30 * super().line_of_cars['Diagnostics']['Quantity']

        return render(request, 'get_ticket/ticket.html', context={
            'ticket_number': ticket_n,
            'waiting_time': waiting_time,
            'oil': super().line_of_cars['Oil']['Quantity'],
            'tires': super().line_of_cars['Tires']['Quantity'],
            'diagnostics': super().line_of_cars['Diagnostics']['Quantity']
        })


class OperatorView(TicketView):
    next_ticket = 0
    def get(self, request, *args, **kwargs):
        global ticket_n, waiting_time
        return render(request, 'processing/processing.html', context={
            'ticket_number': ticket_n,
            'oil': super().line_of_cars['Oil']['Quantity'],
            'tires': super().line_of_cars['Tires']['Quantity'],
            'diagnostics': super().line_of_cars['Diagnostics']['Quantity'],
        })

    def post(self, request, *args, **kwargs):
        if super().line_of_cars['Tires']['Quantity'] > 0 and super().line_of_cars['Tires']['ticket_numbers'][0] == 1:
            super().line_of_cars['Tires']['Quantity'] -= 1
            self.next_ticket = super().line_of_cars['Tires']['ticket_numbers'].pop(0)
        elif super().line_of_cars['Diagnostics']['Quantity'] > 0 and super().line_of_cars['Diagnostics']['ticket_numbers'][0] == 1:
            super().line_of_cars['Diagnostics']['Quantity'] -= 1
            self.next_ticket = super().line_of_cars['Diagnostics']['ticket_numbers'].pop(0)
        elif super().line_of_cars['Oil']['Quantity'] > 0:
            super().line_of_cars['Oil']['Quantity'] -= 1
            self.next_ticket = super().line_of_cars['Oil']['ticket_numbers'].pop(0)
        elif super().line_of_cars['Tires']['Quantity'] > 0:
            super().line_of_cars['Tires']['Quantity'] -= 1
            self.next_ticket = super().line_of_cars['Tires']['ticket_numbers'].pop(0)
        elif super().line_of_cars['Diagnostics']['Quantity'] > 0:
            super().line_of_cars['Diagnostics']['Quantity'] -= 1
            self.next_ticket = super().line_of_cars['Diagnostics']['ticket_numbers'].pop(0)
        else:
            self.next_ticket = 0
        return redirect('/next/')

class NextView(TicketView):
    next_ticket = 0
    def get(self, request, *args, **kwargs):
        if super().line_of_cars['Tires']['Quantity'] > 0 and super().line_of_cars['Tires']['ticket_numbers'][0] == 1:
            self.next_ticket = super().line_of_cars['Tires']['ticket_numbers'][0]
        elif super().line_of_cars['Diagnostics']['Quantity'] > 0 and super().line_of_cars['Diagnostics']['ticket_numbers'][0] == 1:
            self.next_ticket = super().line_of_cars['Diagnostics']['ticket_numbers'][0]
        elif super().line_of_cars['Oil']['Quantity'] > 0:
            self.next_ticket = super().line_of_cars['Oil']['ticket_numbers'][0]
        elif super().line_of_cars['Tires']['Quantity'] > 0:
            self.next_ticket = super().line_of_cars['Tires']['ticket_numbers'][0]
        elif super().line_of_cars['Diagnostics']['Quantity'] > 0:
            self.next_ticket = super().line_of_cars['Diagnostics']['ticket_numbers'][0]
        else:
            self.next_ticket = 0
        return render(request, 'Next/next.html', context={
            'ticket_number': self.next_ticket,
        })
