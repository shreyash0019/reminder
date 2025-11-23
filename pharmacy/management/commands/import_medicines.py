import csv
from django.core.management.base import BaseCommand
from pharmacy.models import Medicine

class Command(BaseCommand):
    help = "Import medicines from a CSV file into the database"

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv',
            type=str,
            default=r"C:\Users\Admin\Downloads\medical_shops_dataset.csv",
            help="Path to the CSV file"
        )

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv']
        try:
            with open(csv_file, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                self.stdout.write(self.style.WARNING(f"CSV Headers: {reader.fieldnames}"))

                count = 0
                for row in reader:
                    Medicine.objects.update_or_create(
                        name=row['medicine_name'],   # ✅ Correct column
                        company=row['manufacturer'],
                        category=row['category'],
                        defaults={
                            "quantity": int(row['quantity']) if row['quantity'] else 0,
                            "price": float(row['price']) if row['price'] else 0.0,
                        }
                    )
                    count += 1

            self.stdout.write(self.style.SUCCESS(f"✅ Successfully imported {count} medicines."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error: {str(e)}"))
