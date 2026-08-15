# ============================================================
# MIGRATION 0002
# AI EV MANAGEMENT SYSTEM - ADDITIONAL FEATURES
# ============================================================

import django.db.models.deletion

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ev_tracking', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [

        # ====================================================
        # 1. AI RECOMMENDATION
        # ====================================================

        migrations.CreateModel(
            name='AIRecommendation',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'recommendation_type',
                    models.CharField(
                        choices=[
                            ('route', 'Route Optimization'),
                            ('charging', 'Charging Recommendation'),
                            ('battery', 'Battery Optimization'),
                            ('traffic', 'Traffic Recommendation'),
                            ('maintenance', 'Maintenance Recommendation'),
                            ('energy', 'Energy Saving Recommendation'),
                        ],
                        max_length=30
                    )
                ),
                ('title', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('confidence_score', models.FloatField(default=0.0)),
                ('is_accepted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                (
                    'vehicle',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='ai_recommendations',
                        to='ev_tracking.evvehicle'
                    )
                ),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),


        # ====================================================
        # 2. TRAFFIC PREDICTION
        # ====================================================

        migrations.CreateModel(
            name='TrafficPrediction',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                ('road_name', models.CharField(max_length=200)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                (
                    'predicted_congestion',
                    models.CharField(
                        choices=[
                            ('low', 'Low'),
                            ('moderate', 'Moderate'),
                            ('high', 'High'),
                            ('severe', 'Severe'),
                        ],
                        max_length=20
                    )
                ),
                ('predicted_vehicle_count', models.IntegerField(default=0)),
                ('predicted_average_speed', models.FloatField(default=0.0)),
                ('confidence_score', models.FloatField(default=0.0)),
                ('prediction_time', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-prediction_time'],
            },
        ),


        # ====================================================
        # 3. ENERGY PREDICTION
        # ====================================================

        migrations.CreateModel(
            name='EnergyPrediction',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                ('predicted_range', models.FloatField()),
                ('predicted_energy_consumption', models.FloatField()),
                ('average_speed', models.FloatField(default=0.0)),
                ('traffic_factor', models.FloatField(default=1.0)),
                ('weather_factor', models.FloatField(default=1.0)),
                ('battery_factor', models.FloatField(default=1.0)),
                ('confidence_score', models.FloatField(default=0.0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                (
                    'vehicle',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='energy_predictions',
                        to='ev_tracking.evvehicle'
                    )
                ),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),


        # ====================================================
        # 4. VEHICLE TELEMETRY
        # ====================================================

        migrations.CreateModel(
            name='VehicleTelemetry',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('speed', models.FloatField(default=0.0)),
                ('battery_percentage', models.FloatField()),
                ('battery_temperature', models.FloatField(default=25.0)),
                ('motor_temperature', models.FloatField(default=25.0)),
                ('energy_consumption', models.FloatField(default=0.0)),
                ('estimated_range', models.FloatField(default=0.0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                (
                    'vehicle',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='telemetry',
                        to='ev_tracking.evvehicle'
                    )
                ),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),


        # ====================================================
        # 5. MAINTENANCE PREDICTION
        # ====================================================

        migrations.CreateModel(
            name='MaintenancePrediction',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'component',
                    models.CharField(
                        choices=[
                            ('battery', 'Battery'),
                            ('motor', 'Electric Motor'),
                            ('brakes', 'Brakes'),
                            ('tyres', 'Tyres'),
                            ('cooling', 'Cooling System'),
                            ('electronics', 'Electronics'),
                        ],
                        max_length=30
                    )
                ),
                (
                    'risk_level',
                    models.CharField(
                        choices=[
                            ('low', 'Low'),
                            ('medium', 'Medium'),
                            ('high', 'High'),
                            ('critical', 'Critical'),
                        ],
                        default='low',
                        max_length=20
                    )
                ),
                ('health_score', models.FloatField(default=100.0)),
                (
                    'predicted_failure_date',
                    models.DateField(
                        blank=True,
                        null=True
                    )
                ),
                ('recommendation', models.TextField(blank=True)),
                ('confidence_score', models.FloatField(default=0.0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                (
                    'vehicle',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='maintenance_predictions',
                        to='ev_tracking.evvehicle'
                    )
                ),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),


        # ====================================================
        # 6. CHARGING STATION PREDICTION
        # ====================================================

        migrations.CreateModel(
            name='ChargingStationPrediction',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                ('predicted_wait_time', models.IntegerField(default=0)),
                (
                    'predicted_available_chargers',
                    models.IntegerField(default=0)
                ),
                ('predicted_demand', models.FloatField(default=0.0)),
                ('confidence_score', models.FloatField(default=0.0)),
                ('prediction_time', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                (
                    'station',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='predictions',
                        to='ev_tracking.chargingstation'
                    )
                ),
            ],
            options={
                'ordering': ['-prediction_time'],
            },
        ),


        # ====================================================
        # 7. SMART TRIP PLANNER
        # ====================================================

        migrations.CreateModel(
            name='TripPlan',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),

                ('origin_name', models.CharField(max_length=200)),
                ('destination_name', models.CharField(max_length=200)),

                ('origin_latitude', models.FloatField()),
                ('origin_longitude', models.FloatField()),

                ('destination_latitude', models.FloatField()),
                ('destination_longitude', models.FloatField()),

                ('estimated_distance', models.FloatField()),
                ('estimated_duration', models.IntegerField()),

                ('estimated_energy_required', models.FloatField()),

                (
                    'estimated_cost',
                    models.DecimalField(
                        max_digits=10,
                        decimal_places=2,
                        default=0
                    )
                ),

                ('charging_stops_required', models.IntegerField(default=0)),
                ('ai_optimized', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),

                (
                    'vehicle',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='trip_plans',
                        to='ev_tracking.evvehicle'
                    )
                ),

                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='trip_plans',
                        to=settings.AUTH_USER_MODEL
                    )
                ),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),


        # ====================================================
        # 8. EMERGENCY / SOS
        # ====================================================

        migrations.CreateModel(
            name='EmergencyEvent',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),

                (
                    'emergency_type',
                    models.CharField(
                        choices=[
                            ('accident', 'Accident'),
                            ('battery', 'Battery Emergency'),
                            ('breakdown', 'Vehicle Breakdown'),
                            ('fire', 'Fire / Overheating'),
                            ('medical', 'Medical Emergency'),
                            ('other', 'Other'),
                        ],
                        max_length=30
                    )
                ),

                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('message', models.TextField(blank=True)),
                ('is_resolved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),

                (
                    'resolved_at',
                    models.DateTimeField(
                        blank=True,
                        null=True
                    )
                ),

                (
                    'vehicle',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='emergency_events',
                        to='ev_tracking.evvehicle'
                    )
                ),

                (
                    'user',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL
                    )
                ),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),


        # ====================================================
        # 9. DRIVING BEHAVIOUR ANALYSIS
        # ====================================================

        migrations.CreateModel(
            name='DrivingAnalysis',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),

                ('average_speed', models.FloatField(default=0.0)),
                ('harsh_accelerations', models.IntegerField(default=0)),
                ('harsh_brakings', models.IntegerField(default=0)),
                ('overspeed_events', models.IntegerField(default=0)),

                (
                    'energy_efficiency_score',
                    models.FloatField(default=100.0)
                ),

                (
                    'driving_score',
                    models.FloatField(default=100.0)
                ),

                ('recommendation', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),

                (
                    'vehicle',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='driving_analysis',
                        to='ev_tracking.evvehicle'
                    )
                ),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]