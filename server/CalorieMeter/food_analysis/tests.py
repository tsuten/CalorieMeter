
from django.test import TestCase
from .services import fallback_classifier, estimate_nutrition, generate_suggestions

class FoodServiceTest(TestCase):
    def test_fallback_classifier(self):
        b = b"dummydata"
        label, score = fallback_classifier(b)
        self.assertIsInstance(label, str)
        self.assertIsInstance(score, float)

    def test_estimate_nutrition(self):
        c, p, carbs, f = estimate_nutrition("pizza")
        self.assertGreater(c, 0)
        self.assertGreaterEqual(p, 0)