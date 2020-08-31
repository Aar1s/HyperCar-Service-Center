from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render

class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('')


class MenuView(View):
    menu = {"Change oil": "change_oil",
                "Inflate tires": "inflate_tires",
                "Get diagnostic test": "diagnostic"}

    def get(self, request, *args, **kwargs):
        return render(request, 'menu.html', context={'menu': self.menu})
