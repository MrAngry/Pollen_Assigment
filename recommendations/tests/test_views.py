from django.test import TestCase, Client
from rest_framework.status import HTTP_404_NOT_FOUND

from rewards.models import RecommendedReward, User
from rewards.serializers import RecommendedRewardSerializer


class TestViews(TestCase):
    def test_recommendations_returns_rewards(self):
        client = Client()

        user = User.objects.create(id=1,name="John Doe",points=100)
        rewards = [RecommendedReward.objects.create(user=user,name='Test Name',points=10,max_per_user=2) for i in range(2)]

        response = client.get(f'/recommendations/{user.id}')
        self.assertSequenceEqual(RecommendedRewardSerializer(rewards,many=True).data,response.json()['rewards'])

    def test_recommendations_returns_404(self):
        client = Client()
        response = client.get(f'/recommendations/1')
        self.assertEquals(response.status_code,HTTP_404_NOT_FOUND)
