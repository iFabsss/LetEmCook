from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
import os

class Command(BaseCommand):
    help = "Sets the default Site domain and name for the current environment."

    def handle(self, *args, **kwargs):
        domain = 'letemcook.onrender.com' if not os.getenv('DEBUG', 'False') == 'True' else 'localhost:8000'
        name = 'Let Em Cook'

        site, created = Site.objects.update_or_create(
            id=1,  # ID 1 is the default site
            defaults={
                'domain': domain,
                'name': name,
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Site with domain: {domain}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Updated Site to domain: {domain}"))
