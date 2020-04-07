from django.core.management.base import BaseCommand
from app.models import LastUpdateDate
from app.views import date


class Command(BaseCommand):
    help = "This command will set current date for scrapper"

    def handle(self, *args, **kwargs):
        LastUpdateDate.objects.create(last_update=date.today())
        self.stdout.write('Last update set on')