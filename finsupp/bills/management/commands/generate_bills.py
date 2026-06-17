from django.core.management.base import BaseCommand
from datetime import date
from ...services import BillService

class Command(BaseCommand):
    help = 'Generate bills for subscriptions due on given date (default today)'

    def add_arguments(self, parser):
        parser.add_argument('--date', type=str, help='Target date YYYY-MM-DD')

    def handle(self, *args, **options):
        target = options.get('date')
        if target:
            target_date = date.fromisoformat(target)
        else:
            target_date = date.today()
        created = BillService.generate_bills_for_date(target_date)
        self.stdout.write(self.style.SUCCESS(f'Created {len(created)} bills'))
