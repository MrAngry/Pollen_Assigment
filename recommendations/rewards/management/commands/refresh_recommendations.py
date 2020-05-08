from django.core.management.base import BaseCommand
from rewards.models import RecommendedReward, User
from rewards.services import HighestRewardsFirstStrategy, RewardsRecommendationStrategy
from rewards.ticketing_api_client import TicketingApiClient


class Command(BaseCommand):
    """Script to refresh recommendations."""

    def handle(self, *args, **options): # No docstring
        from rewards.rewards import REWARDS  # Importing here will allow to patch the value for tests
        client = TicketingApiClient()
        users = client.get_users()
        strategy: RewardsRecommendationStrategy = HighestRewardsFirstStrategy()
        for user_json in users:
            user, _ = User.objects.get_or_create(id=user_json['id'])
            user.points = user_json['points']
            user.save()

            recommended_rewards = strategy.run(user.points, REWARDS)

            RecommendedReward.objects.filter(user=user).delete()
            RecommendedReward.objects.bulk_create([
                RecommendedReward(user=user, **reward) for reward in recommended_rewards
            ])
