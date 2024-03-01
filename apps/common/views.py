from django.shortcuts import render, redirect
from django.views import View

# Create your views here.


class RedirectVIew(View):
    def get(self, request):
        return redirect('api-home')
