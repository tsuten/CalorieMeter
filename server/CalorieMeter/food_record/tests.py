
from django.test import TestCase
from django.contrib.auth.models import User
from users.models import UserProfile
from food_record.models import FoodRecord

class FoodRecordTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        profile = UserProfile.objects.create(user=user)
        FoodRecord.objects.create(user_profile=profile, description='Test Meal')

    def test_record_created(self):
        record = FoodRecord.objects.first()
        self.assertEqual(record.description, 'Test Meal')