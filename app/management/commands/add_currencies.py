from django.core.management.base import BaseCommand
from app.models import Currency


class Command(BaseCommand):
    help = "This command will create 6 most popular currencies"

    def handle(self, *args, **kwargs):
        Currency.objects.create(name='PLN', in_pln=1)
        Currency.objects.create(name='EUR', in_pln=4)
        Currency.objects.create(name='USD', in_pln=4)
        Currency.objects.create(name='GBP', in_pln=5)
        Currency.objects.create(name='NOK', in_pln=0.5)
        Currency.objects.create(name='CHF', in_pln=4)
        self.stdout.write('6 currencies have been added to database.')