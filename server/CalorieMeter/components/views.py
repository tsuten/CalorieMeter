from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import View
# Create your views here.
def index(request):
    return render(request, 'index.html')

class UploadView(View):
    def get(self, request):
        return render(request, 'upload.html')
    def post(self, request):
        print('POSTデータ:', request.POST)
        if not request.FILES:
            return render(request, 'upload.html', {'error': 'ファイルがありません'})
        for _, file in request.FILES.items():
            print(f'ファイル名: {file.name}, コンンテンツタイプ: {file.content_type}')
        return render(request, 'upload.html')

def calendar(request):
    return render(request, 'calendar.html')

# @login_required
def statistics(request):
    return render(request, 'statistics.html')

def profile(request):
    return render(request, 'profile.html')

def record(request):
    return render(request, 'record.html')