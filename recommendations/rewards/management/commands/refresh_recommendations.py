from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Script to refresh recommendations."""

    def handle(self, *args, **options):
        print('This is a test')
