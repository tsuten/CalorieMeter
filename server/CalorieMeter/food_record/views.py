import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import FoodRecord
from users.models import UserProfile
from .forms import FoodRecordForm

logger = logging.getLogger(__name__)

# 写真のアップロードがosライブラリを使用して可能にする
## 現況では不可
@login_required
def record_create(request):
    profile, created = UserProfile.objects.get_or_create(auth=request.user)

    if created:
        logger.info(f"Created new UserProfile for user {request.user.id}")
        
    if request.method == 'POST':
        image_path = request.FILES.get('image_path')
        
        try:
            FoodRecord.objects.create(
                recorded_by=profile,   # UserProfile外部キー
                description="",
                image=image_path,
                recorded_at=timezone.now(),
            )
            logger.info(f"FoodRecord created for {profile.id}")
            # 成功後リロード & food_analysisのanalyze_record処理
            return redirect('food_analysis:analyze_record', record_id=FoodRecord.objects.latest('id').id)
        
        
        except Exception as e: # 例外処理(エラー発生時)
            logger.error(f" Error saving FoodRecord: {e}")
            return render(request, 'upload.html', {
                'error': f"Error saving record: {e}"
            })

    records = FoodRecord.objects.filter(recorded_by=profile).order_by('-recorded_at')
    return render(request, 'upload.html', {'records': records})


@login_required
def record_list(request):
    """
    ログインユーザーの食事記録一覧を表示
    """
    try:
        user_profile = UserProfile.objects.get(auth=request.user)

        records = FoodRecord.objects.filter(
            recorded_by=user_profile
        ).order_by('-recorded_at')

    except UserProfile.DoesNotExist:
        # プロフィールが存在しない場合
        records = []
        user_profile = None

    return render(request, 'meal_info.html', {
        'records': records,
        'user_profile': user_profile,
    })


@login_required
def record_detail(request, record_id):
    record = get_object_or_404(FoodRecord, pk=record_id)
    return render(request, 'detail.html', {'record': record})



# class UploadView(View):
#     def get(self, request):
#         user = AuthAccount.objects.get(id=request.user.id)
#         meals = Meal.objects.filter(uploaded_by=user).order_by('-created_at')
#         return render(request, 'upload.html', {'meals': meals})
    
#     def post(self, request):
#         print('POSTデータ:', request.POST)
#         if not request.FILES:
#             return render(request, 'upload.html', {'error': 'ファイルがありません'})
        
#         uploaded_image_url = None
#         for _, file in request.FILES.items():
#             print(f'ファイル名: {file.name}, コンテンツタイプ: {file.content_type}')
            
#             # ファイルを保存
#             try:
#                 file_extension = os.path.splitext(file.name)[1]
#                 unique_filename = f"{uuid.uuid4()}{file_extension}"
#                 file_path = f"meals/{unique_filename}"
#                 saved_path = default_storage.save(file_path, file)
#                 uploaded_image_url = f"{saved_path}"
#                 print(f'保存されたパス: {uploaded_image_url}')
#                 meal = Meal.objects.create(
#                     name=file.name,
#                     uploaded_by=request.user,
#                     image=uploaded_image_url,
#                     calorie=0,
#                     memo='',
#                 )
#             except Exception as e:
#                 print(f'エラー: {str(e)}')
            
#             # results = classify_food_image(file)
#             # print(results)
        
#         return redirect('meal-info', meal_id=meal.id)