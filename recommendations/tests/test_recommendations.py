"""Recommendations tests.

   We use pytest internally but you can choose a library you're most comfortable with."""

import pytest
import unittest

from rewards.models import TestModel

pytestmark = pytest.mark.django_db

# Those are dummy test which were already present in the assigment
def test_1():
    assert 1 == 1


def test_model():
    test_obj = TestModel.objects.create(test='test')

    assert test_obj.test == 'test'


class TestCase(unittest.TestCase):
     def test_1(self):
         self.assertEqual(1, 1)
