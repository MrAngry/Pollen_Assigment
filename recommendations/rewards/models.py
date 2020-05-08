from django.db import models


class User(models.Model):
    name = models.TextField(null=True)
    points = models.IntegerField(default=0)


class TestModel(models.Model):
    """This is here just as a test, feel free to remove it."""

    test = models.CharField(max_length=100)


class RecommendedReward(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='recommended_rewards')
    name = models.CharField(max_length=100)
    points = models.IntegerField()
    max_per_user = models.IntegerField()
