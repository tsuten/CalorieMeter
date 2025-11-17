from django.shortcuts import render, get_object_or_404
from food_record.models import FoodRecord
from .models import FoodAnalysisResult
from .services import analyze_food_image

def analyze_record(request, record_id):
    record = get_object_or_404(FoodRecord, record_id=record_id)
    result_data = analyze_food_image(record.image.path)

    # 保存処理
    analysis, created = FoodAnalysisResult.objects.update_or_create(
        record=record,
        defaults={
            'predicted_food': result_data['predicted_food'],
            'confidence': result_data['confidence'],
            'nutrients': result_data['nutrients'],
        }
    )

    # FoodRecord側も更新
    record.description = result_data['predicted_food']
    record.calories = result_data['nutrients'].get('calories', 0)
    record.nutrients = result_data['nutrients']
    record.save()

    return render(request, 'result.html', {
        'record': record,
        'analysis': analysis
    })