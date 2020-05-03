from django.db import models


class TestModel(models.Model):
    """This is here just as a test, feel free to remove it."""

    test = models.CharField(max_length=100)
