import csv
from django.core.management.base import BaseCommand
from goshuin.models import Temple

class Command(BaseCommand):
    help = 'Import temple data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        try:
            with open(csv_file, newline='', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                headers = reader.fieldnames
                print(f"Headers: {headers}")  # デバッグ用

                for row in reader:
                    print(f"Row: {row}")  # デバッグ用
                    try:
                        Temple.objects.create(
                            name=row['name'],
                            latitude=row['latitude'],
                            longitude=row['longitude']
                        )
                    except KeyError as e:
                        print(f"KeyError: {e} in row {row}")
        except FileNotFoundError:
            print(f"File not found: {csv_file}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
