from django.core.management.base import BaseCommand

from ticketing_api.models import User, Ticket, Order

class Command(BaseCommand):
    """Set up useful data for testing."""

    def handle(self, *args, **options):
        # Add users
        User.objects.create(
            id=1,
            name='John Doe',
            points=100,
        )
        User.objects.create(
            id=2,
            name='Jane Doe',
            points=150,
        )

        # Add tickets
        cheap_ticket = Ticket.objects.create(
            id=1,
            name='Cheap ticket',
            price=20,
            reward_points=50,
        )
        expensive_ticket = Ticket.objects.create(
            id=2,
            name='Expensive ticket',
            price=50,
            reward_points=100,
        )

        # Add orders
        order_1 = Order.objects.create(
            id=1,
            user_id=1,
        )
        order_1.tickets.add(expensive_ticket)

        order_2 = Order.objects.create(
            id=2,
            user_id=2,
        )
        order_2.tickets.add(cheap_ticket)
        order_2.tickets.add(expensive_ticket)
