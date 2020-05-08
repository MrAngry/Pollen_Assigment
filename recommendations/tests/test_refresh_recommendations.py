from unittest.mock import patch
from django.core.management import call_command
from django.db.models import Sum
from django.test import TestCase

from rewards import ticketing_api_client
from rewards.models import RecommendedReward, User

DUMMY_USER = dict(id=1, name='John Doe', points=4)


@patch.object(ticketing_api_client.TicketingApiClient, 'get_users',
              return_value=[DUMMY_USER])
class TestCommand(TestCase): # General tests independent of recommendation strategy that was used
    def test_handle_old_recommendations_are_removed(self, get_users_mock):
        user = User.objects.create(name="John Doe", points=1)
        reward = RecommendedReward.objects.create(user=user, name='TEST', points=1, max_per_user=1)
        call_command('refresh_recommendations')
        self.assertNotIn(reward, user.recommended_rewards.all())

    @patch('rewards.rewards.REWARDS', new=[{"name": "Test Ticket", "points": 1, "max_per_user": 4}])
    def test_handle_points_are_exhausted(self, get_users_mock):
        call_command('refresh_recommendations')
        self.assertEquals(User.objects.get(id=DUMMY_USER['ID']).points,
                          RecommendedReward.objects.filter(user_id=DUMMY_USER['ID']).aggregate(Sum('points'))[
                              'points__sum'])

    @patch('rewards.rewards.REWARDS', new=[{"name": "Test Ticket", "points": 1, "max_per_user": 2}])
    def test_handle_max_usage_limit_is_kept(self, get_users_mock):
        call_command('refresh_recommendations')
        self.assertEquals(2, RecommendedReward.objects.filter(user_id=DUMMY_USER['ID']).aggregate(Sum('points'))[
            'points__sum'])
