"""This just an example. You're not expected to make any changes here."""

import pytest

from ticketing_api.models import Ticket

pytestmark = pytest.mark.django_db


def test_ticket():
    ticket = Ticket.objects.create(name='ticket', price=2.30, reward_points=100)

    assert ticket.name == 'ticket'
