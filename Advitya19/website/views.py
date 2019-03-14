from django.shortcuts import render

def events(request):
    return render(request, 'website/events/index.html', {})

def home(request):
    return render(request, 'website/home/index.html', {})