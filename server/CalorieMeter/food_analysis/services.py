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