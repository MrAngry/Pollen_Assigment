from django.conf import settings
from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.TextField(null=True)
    points = models.IntegerField()


class Ticket(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    reward_points = models.IntegerField()


class Order(models.Model):
    user_id = models.IntegerField()
    tickets = models.ManyToManyField(Ticket)
