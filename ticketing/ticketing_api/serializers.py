from ticketing_api.models import Order

from rest_framework import serializers


class TicketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    price = serializers.FloatField()
    reward_points = serializers.IntegerField()

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    points = serializers.IntegerField()

class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    tickets = TicketSerializer(many=True)
