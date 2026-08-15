from django.core.management.base import BaseCommand
from django.utils import timezone
from ev_tracking.models import EVVehicle, ChargingStation, Alert, TrafficSnapshot
from ev_tracking.india_config import INDIAN_VEHICLE_MODELS, SAMPLE_CHARGING_STATIONS, INDIAN_EXPRESSWAYS
import random
import time


class Command(BaseCommand):
    help = 'Simulate EV traffic and charging events'

    def add_arguments(self, parser):
        parser.add_argument('--duration', type=int, default=3600, help='Duration in seconds')
        parser.add_argument('--interval', type=int, default=5, help='Update interval in seconds')
        parser.add_argument('--vehicles', type=int, default=50, help='Number of vehicles to simulate')

    def handle(self, *args, **options):
        duration = options['duration']
        interval = options['interval']
        num_vehicles = options['vehicles']

        # Create vehicles if they don't exist
        vehicles = list(EVVehicle.objects.all())
        if len(vehicles) < num_vehicles:
            self.stdout.write(f"Creating {num_vehicles - len(vehicles)} vehicles...")
            # Use Delhi-Jaipur expressway as primary zone
            delhi_jaipur = INDIAN_EXPRESSWAYS['delhi_jaipur']
            start_lat, start_lon = delhi_jaipur['start']
            end_lat, end_lon = delhi_jaipur['end']
            
            for i in range(num_vehicles - len(vehicles)):
                # Spread vehicles across expressway
                lat = start_lat + (end_lat - start_lat) * random.random()
                lon = start_lon + (end_lon - start_lon) * random.random()
                
                vehicle = EVVehicle.objects.create(
                    vehicle_type=random.choice(INDIAN_VEHICLE_MODELS),
                    battery_capacity=75.0,
                    current_charge=random.uniform(20, 75),
                    latitude=lat,
                    longitude=lon,
                    speed=random.uniform(0, 100),
                    status=random.choice(['idle', 'driving', 'charging'])
                )
                vehicles.append(vehicle)

        # Create charging stations if they don't exist
        stations = list(ChargingStation.objects.all())
        if len(stations) == 0:
            self.stdout.write("Creating Indian charging stations...")
            for station_data in SAMPLE_CHARGING_STATIONS:
                ChargingStation.objects.create(
                    name=station_data['name'],
                    latitude=station_data['lat'],
                    longitude=station_data['lon'],
                    chargers_available=random.randint(1, 3),
                    chargers_total=random.randint(3, 6),
                    charger_type=station_data['charger_type'],
                    power_capacity=station_data['power_capacity'],
                    amenities=station_data['amenities'],
                )
            # Reload stations
            stations = list(ChargingStation.objects.all())

            # Reload stations after creation
            stations = list(ChargingStation.objects.all())

        self.stdout.write(self.style.SUCCESS(f'Starting simulation with {len(vehicles)} vehicles...'))

        elapsed = 0
        while elapsed < duration:
            for vehicle in vehicles:
                # Update vehicle location and battery
                lat_change = random.uniform(-0.001, 0.001)
                lon_change = random.uniform(-0.001, 0.001)
                vehicle.latitude += lat_change
                vehicle.longitude += lon_change

                # Random speed changes
                vehicle.speed = max(0, min(120, vehicle.speed + random.uniform(-10, 10)))

                # Battery depletion based on speed
                if vehicle.status == 'driving':
                    battery_loss = (vehicle.speed / 100) * 0.1
                    vehicle.current_charge = max(0, vehicle.current_charge - battery_loss)
                    
                    # Randomly switch to charging if low battery
                    if vehicle.current_charge < 20:
                        vehicle.status = 'charging'
                        vehicle.speed = 0
                elif vehicle.status == 'charging':
                    # Charge battery
                    charge_gain = random.uniform(2, 5)
                    vehicle.current_charge = min(vehicle.battery_capacity, vehicle.current_charge + charge_gain)
                    
                    # If charged, resume driving
                    if vehicle.current_charge > 70:
                        vehicle.status = 'driving'
                        vehicle.speed = random.uniform(20, 100)

                vehicle.save()

                # Generate alerts based on vehicle state
                if vehicle.current_charge < 20 and vehicle.status != 'charging':
                    Alert.objects.get_or_create(
                        vehicle=vehicle,
                        alert_type='low_battery',
                        resolved=False,
                        defaults={
                            'message': f'Battery critically low: {round(vehicle.battery_percentage())}%',
                            'severity': 'high'
                        }
                    )

                if vehicle.current_charge > 70 and Alert.objects.filter(
                    vehicle=vehicle, alert_type='low_battery', resolved=False
                ).exists():
                    alerts = Alert.objects.filter(vehicle=vehicle, alert_type='low_battery', resolved=False)
                    for alert in alerts:
                        alert.resolve()

            # Create traffic snapshot every 30 seconds
            if elapsed % 30 == 0:
                driving_vehicles = len([v for v in vehicles if v.status == 'driving'])
                avg_speed = sum([v.speed for v in vehicles]) / len(vehicles) if vehicles else 0
                
                congestion = 'clear'
                if avg_speed < 30:
                    congestion = 'heavy'
                elif avg_speed < 60:
                    congestion = 'moderate'

                TrafficSnapshot.objects.create(
                    expressway_section='I-80 East',
                    timestamp=timezone.now(),
                    vehicle_count=driving_vehicles,
                    average_speed=round(avg_speed, 2),
                    congestion_level=congestion
                )

            elapsed += interval
            time.sleep(interval)

        self.stdout.write(self.style.SUCCESS('Simulation completed'))
