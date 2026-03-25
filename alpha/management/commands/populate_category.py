from alpha.models import Category
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help="This command inserts category data"

    def handle(self, *args, **options):
        Category.objects.all().delete()
       
        Categories=["Sports","Food","Tecchnology","Science","Art"]

        for Category_name in Categories:
            Category.objects.create(name=Category_name)

        self.stdout.write(self.style.SUCCESS("Completed inserting data !"))
