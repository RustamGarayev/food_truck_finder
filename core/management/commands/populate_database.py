import csv
import sys

from django.core.management.base import BaseCommand
from core.models import FoodTruck


FACILITY_TYPE_MAP = {
    "Truck": "T",
    "Push Cart": "P",
}


class Command(BaseCommand):
    help = """ Load a list of food trucks from a CSV file into the database
        path to the CSV file should be passed as an argument
        e.g. python manage.py populate_database --path /path/to/food-truck-data.csv
        if no argument is passed, the command will fail with a message like:
            Error: This command requires exactly one named argument: the path to the CSV file!
    """

    def add_arguments(self, parser):
        parser.add_argument("--path")

    def handle(self, *args, **kwargs):
        csv_path = self._get_csv_path()

        # DictReader reference: https://docs.python.org/3/library/csv.html#csv.DictReader
        with open(csv_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Create and save FoodTruck instance
                FoodTruck.objects.get_or_create(
                    name=row["Applicant"],
                    facility_type=FACILITY_TYPE_MAP.get(row["FacilityType"], "N/A"),
                    location_description=row["LocationDescription"],
                    address=row["Address"],
                    latitude=float(row["Latitude"]),
                    longitude=float(row["Longitude"]),
                )

        self.stdout.write(self.style.SUCCESS("Data imported successfully"))

    def _get_csv_path(self):
        # Check if csv_path argument was passed
        if len(sys.argv) == 4:
            # Get csv_path from command line argument
            return sys.argv[-1]
        else:
            self.stdout.write(
                self.style.ERROR(
                    "This command requires exactly one named argument: the path to the CSV file!\n"
                    "Example Usage:\n"
                    "\tpython manage.py populate_database --path <path_to_csv_file>\n"
                    "Check the help text for more information."
                )
            )
            sys.exit(1)
