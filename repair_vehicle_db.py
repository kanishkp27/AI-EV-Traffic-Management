import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ev_management.settings")

import django
django.setup()

from django.db import connection


columns = [
    ("registration_number", "varchar(50) NOT NULL DEFAULT ''"),
    ("color", "varchar(50) NOT NULL DEFAULT ''"),
    ("registration_year", "integer NULL"),
    ("mileage", "real NOT NULL DEFAULT 0.0"),
    ("vin", "varchar(100) NULL"),
    ("manufacturer", "varchar(100) NOT NULL DEFAULT ''"),
    ("model_name", "varchar(100) NOT NULL DEFAULT ''"),
    ("battery_temperature", "real NOT NULL DEFAULT 25.0"),
    ("estimated_range", "real NOT NULL DEFAULT 0.0"),
    ("odometer", "real NOT NULL DEFAULT 0.0"),
    ("is_active", "bool NOT NULL DEFAULT 1"),
]


with connection.cursor() as cursor:

    cursor.execute("PRAGMA table_info(ev_tracking_evvehicle)")
    existing = {row[1] for row in cursor.fetchall()}

    print("\nExisting columns:")
    for column in sorted(existing):
        print(" -", column)

    print("\nRepairing table...\n")

    for name, definition in columns:

        if name in existing:
            print("EXISTS:", name)
            continue

        sql = (
            f"ALTER TABLE ev_tracking_evvehicle "
            f"ADD COLUMN {name} {definition}"
        )

        cursor.execute(sql)

        print("ADDED:", name)


print("\nEVVehicle table repair complete.")


with connection.cursor() as cursor:

    cursor.execute("PRAGMA table_info(ev_tracking_evvehicle)")

    print("\nFinal database columns:\n")

    for row in cursor.fetchall():
        print(row)


from ev_tracking.models import EVVehicle

print("\nTesting EVVehicle model...")

try:
    print("Vehicle count:", EVVehicle.objects.count())

    vehicles = EVVehicle.objects.all()[:5]

    for vehicle in vehicles:
        print(
            "Vehicle:",
            vehicle.id,
            vehicle.vehicle_type,
            vehicle.registration_number
        )

    print("\nSUCCESS: EVVehicle model can access the database.")

except Exception as error:

    print("\nMODEL TEST FAILED:")
    print(error)