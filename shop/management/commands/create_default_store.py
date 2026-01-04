"""
Management command to create an initial default store
for existing data migration
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Store


class Command(BaseCommand):
    help = 'Create a default store for migration purposes'

    def handle(self, *args, **options):
        # Get or create admin user
        admin = User.objects.filter(is_superuser=True).first()
        if not admin:
            admin = User.objects.filter(is_staff=True).first()
        if not admin:
            admin = User.objects.first()
        
        if not admin:
            self.stdout.write(self.style.ERROR('No users found. Please create a user first.'))
            return
        
        # Create default store
        store, created = Store.objects.get_or_create(
            slug='default-store',
            defaults={
                'name': 'Default Store',
                'description': 'Default store for existing products',
                'owner': admin,
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created default store with ID: {store.id}'))
        else:
            self.stdout.write(self.style.WARNING(f'Default store already exists with ID: {store.id}'))
