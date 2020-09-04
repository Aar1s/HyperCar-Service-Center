from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from collections import deque
import datetime
ticket_n = 0
counter = 0
waiting_time = 0


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


class TicketView(View):
    line_of_cars = {'Oil': {'Quantity': 0, 'ticket_numbers': []},
                'Tires': {'Quantity': 0, 'ticket_numbers': []},
                'Diagnostics': {'Quantity': 0, 'ticket_numbers': []}}
    tickets = {'tickets': []}

    def find_next_ticket(self):
        global counter
        if self.line_of_cars['Oil']['Quantity'] > 0:
            next_ticket = self.line_of_cars['Oil']['ticket_numbers'][0]
        elif self.line_of_cars['Tires']['Quantity'] > 0:
            next_ticket = self.line_of_cars['Tires']['ticket_numbers'][0]
        elif self.line_of_cars['Diagnostics']['Quantity'] > 0:
            next_ticket = self.line_of_cars['Diagnostics']['ticket_numbers'][0]
        else:
            next_ticket = 0
        if counter == 0:
            next_ticket = 1
            counter += 1
        self.tickets['tickets'].append(next_ticket)
        if len(self.tickets['tickets']) < 3:
            current_ticket = self.tickets['tickets'][-1]
        else:
            current_ticket = self.tickets['tickets'][-2]
        return next_ticket, current_ticket


class OilView(TicketView):
    def get(self, request, *args, **kwargs):
        global ticket_n, waiting_time
        ticket_n += 1
        super().line_of_cars['Oil']['Quantity'] += 1
        super().line_of_cars['Oil']['ticket_numbers'].append(ticket_n)
        if ticket_n <= 2:
            waiting_time = 0
        else:
            waiting_time = 2 * (super().line_of_cars['Oil']['Quantity'])
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
            waiting_time = 2 * (super().line_of_cars['Tires']['Quantity']) +\
                           5 * (super().line_of_cars['Tires']['Quantity'])

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
        else:
            waiting_time = 2 * super().line_of_cars['Tires']['Quantity'] +\
                           5 * super().line_of_cars['Tires']['Quantity'] +\
                           30 * (super().line_of_cars['Tires']['Quantity'])
        return render(request, 'get_ticket/ticket.html', context={
            'ticket_number': ticket_n,
            'waiting_time': waiting_time,
            'oil': super().line_of_cars['Oil']['Quantity'],
            'tires': super().line_of_cars['Tires']['Quantity'],
            'diagnostics': super().line_of_cars['Diagnostics']['Quantity']
        })


class OperatorView(TicketView):
    def get(self, request, *args, **kwargs):
        global ticket_n, waiting_time
        return render(request, 'processing/processing.html', context={
            'ticket_number': ticket_n,
            'oil': super().line_of_cars['Oil']['Quantity'],
            'tires': super().line_of_cars['Tires']['Quantity'],
            'diagnostics': super().line_of_cars['Diagnostics']['Quantity'],
        })

    def post(self, request, *args, **kwargs):
        next_ticket = super().find_next_ticket()[0]
        for key, value in super().line_of_cars.items():
            if value['Quantity'] > 0:
                for ticket in value['ticket_numbers']:
                    if ticket == next_ticket:
                        print(super().line_of_cars[key]['ticket_numbers'].pop(0))
                        super().line_of_cars[key]['Quantity'] -= 1
        return redirect('/')


class NextView(TicketView):
    global ticket_n

    def get(self, request, *args, **kwargs):
        next_ticket, current_ticket = super().find_next_ticket()
        if ticket_n > 2:
            busy = True
        else:
            busy = False
        return render(request, 'Next/next.html', context={
            'ticket_number': current_ticket,
            'busy': busy,
        })
