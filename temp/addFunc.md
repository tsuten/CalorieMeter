
⸻

🍱 CalörieMeter: Djangoアプリ構成（food_record & food_analysis 分割版）

環境
	•	Python: 3.10+
	•	Django: 4.2+
	•	モデル間リレーション:
	•	UserProfile → FoodRecord（1対多）
	•	FoodRecord → FoodAnalysisResult（1対1）

⸻




⸻

food_record/models.py

from django.db import models
from user.models import UserProfile

class FoodRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    user_profile = models.ForeignKey(
        UserProfile,
        to_field='user_id',             # ← user_idを外部キーに指定
        db_column='user_id',
        on_delete=models.CASCADE,
        related_name="food_records"
    )
    image = models.ImageField(upload_to='food_images/')
    description = models.TextField(blank=True, null=True)
    calories = models.FloatField(blank=True, null=True)
    nutrients = models.JSONField(blank=True, null=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Record {self.record_id} (UserID: {self.user_profile.user_id})"

⸻

food_analysis/models.py

from django.db import models
from food_record.models import FoodRecord

class FoodAnalysisResult(models.Model):
    record = models.OneToOneField(FoodRecord, on_delete=models.CASCADE, related_name='analysis')
    predicted_food = models.CharField(max_length=100)
    confidence = models.FloatField()
    nutrients = models.JSONField()
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for Record {self.record.record_id}"


⸻

4️⃣ food_record/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FoodRecord
from user.models import UserProfile
from .forms import FoodRecordForm

@login_required
def record_list(request):
    profile = UserProfile.objects.get(user=request.user)
    records = FoodRecord.objects.filter(user_profile=profile).order_by('-recorded_at')
    return render(request, 'food_record/record_list.html', {'records': records})

@login_required
def record_create(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = FoodRecordForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.user_profile = profile
            record.save()
            return redirect('food_record:record_list')
    else:
        form = FoodRecordForm()
    return render(request, 'food_record/record_form.html', {'form': form})

@login_required
def record_detail(request, record_id):
    record = get_object_or_404(FoodRecord, record_id=record_id)
    return render(request, 'food_record/record_detail.html', {'record': record})


⸻

5️⃣ food_analysis/views.py

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

    return render(request, 'food_analysis/analysis_result.html', {
        'record': record,
        'analysis': analysis
    })


⸻

6️⃣ food_analysis/services.py

from transformers import pipeline
from PIL import Image
import json

# --- Hugging Faceモデルの読み込み ---
# 事前学習済み食事分類モデル
classifier = pipeline("image-classification", model="nateraw/food")

def analyze_food_image(image_path):
    """
    画像をHuggingFaceのnateraw/foodモデルで解析
    """
    img = Image.open(image_path).convert("RGB")
    results = classifier(img)

    if not results:
        return {
            "predicted_food": "unknown",
            "confidence": 0.0,
            "nutrients": estimate_nutrients("unknown")
        }

    top = results[0]
    predicted_food = top["label"]
    confidence = float(top["score"])

    return {
        "predicted_food": predicted_food,
        "confidence": confidence,
        "nutrients": estimate_nutrients(predicted_food)
    }


def estimate_nutrients(food_name):
    """
    栄養素の簡易データ
    """
    data = {
        "rice": {"calories": 130, "protein": 2.7, "fat": 0.3, "carbs": 28},
        "pizza": {"calories": 285, "protein": 12, "fat": 10, "carbs": 36},
        "salad": {"calories": 80, "protein": 1.2, "fat": 3.4, "carbs": 11},
        "ramen": {"calories": 500, "protein": 16, "fat": 20, "carbs": 65},
        "unknown": {"calories": 0, "protein": 0, "fat": 0, "carbs": 0}
    }
    return data.get(food_name.lower(), data["unknown"])

# --- 将来のSageMaker推論呼び出し ---
"""
def analyze_food_image_sagemaker(image_path):
    import requests
    import json

    endpoint_url = "https://your-sagemaker-endpoint.amazonaws.com/invocations"
    payload = json.dumps({"image_path": image_path})
    headers = {"Content-Type": "application/json"}

    response = requests.post(endpoint_url, data=payload, headers=headers)
    result = response.json()
    return result
"""

⸻

7️⃣ food_record/forms.py

from django import forms
from .models import FoodRecord

class FoodRecordForm(forms.ModelForm):
    class Meta:
        model = FoodRecord
        fields = ['image']


⸻

8️⃣ URL設定

food_record/urls.py

from django.urls import path
from . import views

app_name = 'food_record'

urlpatterns = [
    path('', views.record_list, name='record_list'),
    path('new/', views.record_create, name='record_create'),
    path('<int:record_id>/', views.record_detail, name='record_detail'),
]

food_analysis/urls.py

from django.urls import path
from . import views

app_name = 'food_analysis'

urlpatterns = [
    path('<int:record_id>/analyze/', views.analyze_record, name='analyze_record'),
]


⸻

9️⃣ HTMLテンプレート構成

📁 templates/food_record/record_list.html

<h2>食事記録一覧</h2>
<a href="{% url 'food_record:record_create' %}">新規記録</a>
<ul>
  {% for record in records %}
  <li>
    <a href="{% url 'food_record:record_detail' record.record_id %}">
      {{ record.recorded_at }} - {{ record.description|default:"未解析" }}
    </a>
  </li>
  {% endfor %}
</ul>


⸻

📁 templates/food_record/record_form.html

<h2>食事を記録</h2>
<form method="post" enctype="multipart/form-data">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">保存</button>
</form>


⸻

📁 templates/food_record/record_detail.html

<h2>食事詳細</h2>
<img src="{{ record.image.url }}" alt="Food Image" width="300">
<p>説明: {{ record.description|default:"未解析" }}</p>
<p>カロリー: {{ record.calories|default:"-" }} kcal</p>
<a href="{% url 'food_analysis:analyze_record' record.record_id %}">AIで解析</a>


⸻

📁 templates/food_analysis/analysis_result.html

<h2>解析結果</h2>
<img src="{{ record.image.url }}" alt="Food Image" width="300">
<p>判定結果: {{ analysis.predicted_food }}</p>
<p>信頼度: {{ analysis.confidence|floatformat:2 }}</p>
<p>栄養素: {{ analysis.nutrients }}</p>
<a href="{% url 'food_record:record_list' %}">一覧へ戻る</a>


⸻

🔟 tests.py（サンプルテスト）

from django.test import TestCase
from django.contrib.auth.models import User
from user.models import UserProfile
from food_record.models import FoodRecord

class FoodRecordTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        profile = UserProfile.objects.create(user=user)
        FoodRecord.objects.create(user_profile=profile, description='Test Meal')

    def test_record_created(self):
        record = FoodRecord.objects.first()
        self.assertEqual(record.description, 'Test Meal')


⸻

✅ この構成のポイント

分類	説明
責務分離	記録（food_record）とAI推論（food_analysis）を完全分離
拡張性	food_analysisは将来的にSageMakerやHugging Face APIを切替可能
API設計	food_analysisが独立したREST API化にも対応しやすい
テスト容易性	各アプリを単独でテスト・CI導入が可能
AWS移行準備	food_analysis → SageMaker、food_record → EC2 + RDS に自然移行可能




yourproject/
├─ food_recognition/
│  ├─ __init__.py
│  ├─ apps.py
│  ├─ models.py
│  ├─ services.py
│  ├─ views.py
│  ├─ urls.py
│  ├─ serializers.py
│  └─ templates/food_recognition/...
├─ notification/
│  ├─ __init__.py
│  ├─ apps.py
│  ├─ models.py
│  ├─ tasks.py
│  ├─ views.py
│  ├─ urls.py
│  └─ templates/notification/...
├─ core/   # 既存の食事モデルなどがある想定
├─ settings.py
└─ manage.py


6) マイグレーション / 初期化

ターミナルで：

python manage.py makemigrations food_recognition notification
python manage.py migrate

管理ユーザー作成・開発起動：

python manage.py createsuperuser
python manage.py runserver


⸻

7) API の使い方（例）
	•	画像を Ajax で送って解析したい場合は /food_recognition/api/analyze/ に multipart/form-data で image を POST。
	•	結果 JSON が帰ってくるのでフロント側で表示可能。

⸻

8) AWS 移行時のポイント（設計メモ）
	•	Hugging Face推論：
	•	開発：HF Inference API（トークン経由）を利用。
	•	本番：SageMaker へモデルデプロイ（推奨）。services.call_hf_inference を SageMaker呼び出しに差替えれば移行容易です。
	•	通知：
	•	開発：Django のメールコンソールを利用。
	•	本番：AWS SES（メール送信）、SNS（SMS/Push）に切り替え。非同期は SQS/Celery on ECS or Lambda へ。
	•	ファイル保管：画像は S3 へ。RecognitionResult.image_s3_url にURLを保存。
	•	非同期処理：分析やメールは非同期に（Celery + Redis / RabbitMQ） → AWS では SQS + Lambda / Fargate へ置換可能。

⸻


🧩 各アプリの役割と責務

アプリ名	主な機能	技術・処理内容
food_record	食事の記録管理	- 食事写真のアップロード- 撮影日時・内容・栄養素・カロリーを保存- データの履歴表示（一覧・詳細）
food_analysis	食事解析・推測・提案	- Hugging Face モデル（nateraw/food）をSageMaker経由で呼び出し- 食材・料理名の自動推測- AIが算出した栄養素を返却- ユーザー嗜好に基づく食事提案生成


⸻

🧠 この構成のメリット

メリット	説明
責務分離	記録機能とAI推測機能を独立して開発・テスト可能
スケーラビリティ	food_analysis は将来的にSageMakerやHugging FaceのAPIを切り替えても、food_record に影響なし
クラウド移行が容易	AI解析部分をAWS（SageMaker・Lambda）に移行してもローカル側はAPI通信だけで済む
再利用性	food_analysis は他のアプリ（例：通知機能・統計機能）からも呼び出し可能
CI/CD対応	解析系と記録系を別リポジトリで管理可能（学習とアプリを分離）


⸻

☁️ AWS 移行時の構成（想定）

層	サービス	内容
バックエンド	EC2（Django）	food_recordアプリなどをホスト
AI解析	SageMaker	food_analysis内の推測モデルを稼働
データベース	RDS (PostgreSQL)	食事記録・ユーザーデータ
ストレージ	S3	画像・AI推論結果の保存
通知・分析	SNS + CloudWatch	通知・監視・ログ収集


from transformers import pipeline
from PIL import Image
import json

# --- Hugging Faceモデルの読み込み ---
# 事前学習済み食事分類モデル
classifier = pipeline("image-classification", model="nateraw/food")

def analyze_food_image(image_path):
    """
    画像をHuggingFaceのnateraw/foodモデルで解析
    """
    img = Image.open(image_path).convert("RGB")
    results = classifier(img)

    if not results:
        return {
            "predicted_food": "unknown",
            "confidence": 0.0,
            "nutrients": estimate_nutrients("unknown")
        }

    top = results[0]
    predicted_food = top["label"]
    confidence = float(top["score"])

    return {
        "predicted_food": predicted_food,
        "confidence": confidence,
        "nutrients": estimate_nutrients(predicted_food)
    }


def estimate_nutrients(food_name):
    """
    栄養素の簡易データ
    """
    data = {
        "rice": {"calories": 130, "protein": 2.7, "fat": 0.3, "carbs": 28},
        "pizza": {"calories": 285, "protein": 12, "fat": 10, "carbs": 36},
        "salad": {"calories": 80, "protein": 1.2, "fat": 3.4, "carbs": 11},
        "ramen": {"calories": 500, "protein": 16, "fat": 20, "carbs": 65},
        "unknown": {"calories": 0, "protein": 0, "fat": 0, "carbs": 0}
    }
    return data.get(food_name.lower(), data["unknown"])

# --- 将来のSageMaker推論呼び出し ---
"""
def analyze_food_image_sagemaker(image_path):
    import requests
    import json

    endpoint_url = "https://your-sagemaker-endpoint.amazonaws.com/invocations"
    payload = json.dumps({"image_path": image_path})
    headers = {"Content-Type": "application/json"}

    response = requests.post(endpoint_url, data=payload, headers=headers)
    result = response.json()
    return result
"""