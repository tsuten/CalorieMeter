from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.core.files.storage import default_storage
from django.conf import settings
import os
import uuid
from core.models import Meal
from users.models import AuthAccount
# from .utils import classify_food_image
# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

class UploadView(View):
    @login_required
    def get(self, request):
        user = AuthAccount.objects.get(id="47a2978c-9294-4179-86ac-878a7e41501b")
        meals = Meal.objects.filter(uploaded_by=user).order_by('-created_at')
        for meal in meals:
            if meal.date_eaten is None and meal.time_eaten is None:
                meal.date_eaten = "未記入"
                meal.time_eaten = ""
        return render(request, 'upload.html', {'meals': meals})
    
    def post(self, request):
        print('POSTデータ:', request.POST)
        if not request.FILES:
            return render(request, 'upload.html', {'error': 'ファイルがありません'})
        
        uploaded_image_url = None
        for _, file in request.FILES.items():
            print(f'ファイル名: {file.name}, コンテンツタイプ: {file.content_type}')
            
            # ファイルを保存
            try:
                file_extension = os.path.splitext(file.name)[1]
                unique_filename = f"{uuid.uuid4()}{file_extension}"
                file_path = f"meals/{unique_filename}"
                saved_path = default_storage.save(file_path, file)
                uploaded_image_url = f"{saved_path}"
                print(f'保存されたパス: {uploaded_image_url}')
                meal = Meal.objects.create(
                    name=file.name,
                    uploaded_by=request.user,
                    image=uploaded_image_url,
                    calorie=0,
                    memo='',
                )
            except Exception as e:
                print(f'エラー: {str(e)}')
            
            # results = classify_food_image(file)
            # print(results)
        
        return redirect('meal-info', meal_id=meal.id)

def calendar(request):
    return render(request, 'calendar.html')

@login_required
def statistics(request):
    return render(request, 'statistics.html')

def profile(request):
    return render(request, 'profile.html')

def record(request):
    return render(request, 'record.html')