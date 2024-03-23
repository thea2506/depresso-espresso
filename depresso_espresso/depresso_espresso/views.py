
from django.shortcuts import render, redirect


def redirect(request):
    return redirect('/site')


def front_end(request):
    return render(request, 'index.html')
