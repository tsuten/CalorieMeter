from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request, 'index.html')

def upload(request):
    return render(request, 'upload.html')

def calendar(request):
    return render(request, 'calendar.html')

@login_required
def statistics(request):
    return render(request, 'statistics.html')