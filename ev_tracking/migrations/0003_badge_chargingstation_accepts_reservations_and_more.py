# ============================================================
# MIGRATION 0003
# EV TRACKING
# ============================================================

from django.db import migrations


class Migration(migrations.Migration):

    # ========================================================
    # DEPENDENCIES
    # ========================================================

    dependencies = [
        (
            'ev_tracking',
            '0002_weatherdata_batteryanalysis_chargingbooking_and_more'
        ),
    ]

    # ========================================================
    # OPERATIONS
    # ========================================================

    operations = []