import abc
from typing import List, Dict


class RewardsRecommendationStrategy(abc.ABC):
    def run(self,points:int,rewards):
        pass


class HighestRewardsFirstStrategy(RewardsRecommendationStrategy):
    def run(self,points:int,rewards:List[Dict]) -> List[Dict]:
        """
        :param points:  Number of points to use for rewards
        :param rewards: A list of dictionaries with two mandatory fields `points` and `max_per_user`
        :return:
        """
        sorted_rewards = sorted(rewards,key=lambda reward: reward['points'])
        result = []
        while sorted_rewards and points > 0:
            reward = sorted_rewards.pop()
            used = 0
            while reward['max_per_user'] > used and reward['points'] <= points:
                used += 1
                points -= reward['points']
                result.append(reward)
        return result
