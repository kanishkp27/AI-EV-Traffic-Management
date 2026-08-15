# Quick Start Guide - EV Management System

## First Time Setup (5 minutes)

### 1. Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup
```bash
# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
# Enter username, email, password when prompted
```

### 3. Generate Demo Data
```bash
# Create 30 sample vehicles and 5 charging stations
python manage.py simulate_traffic --vehicles 30 --duration 20 --interval 2
```

### 4. Start Development Server
```bash
python manage.py runserver
```

The server will start at `http://localhost:8000`

## Web Interface Access

### Dashboard Pages
1. **Driver Dashboard** - http://localhost:8000/
   - Real-time vehicle locations on map
   - Active alerts
   - Fleet statistics

2. **Charging Station Finder** - http://localhost:8000/charging-finder/
   - Search stations by location
   - Availability indicators
   - Distance calculations

3. **Route Planner** - http://localhost:8000/route-planner/
   - Plan routes between locations
   - Get charging stop recommendations
   - View energy requirements

4. **Admin Dashboard** - http://localhost:8000/admin-dashboard/
   - Fleet analytics
   - Traffic flow data
   - Battery health distribution
   - Real-time statistics

## API Usage

### Get All Vehicles
```bash
curl http://localhost:8000/api/vehicles/
```

### Find Nearby Charging Stations
```bash
curl "http://localhost:8000/api/stations/nearby/?lat=37.7749&lon=-122.4194&radius=50"
```

### Suggest Route with Charging Stops
```bash
curl -X POST http://localhost:8000/api/routes/suggest/ \
  -H "Content-Type: application/json" \
  -d '{
    "origin_lat": 37.7749,
    "origin_lon": -122.4194,
    "destination_lat": 37.3382,
    "destination_lon": -121.8863,
    "current_battery": 75,
    "battery_capacity": 75
  }'
```

### Get Active Alerts
```bash
curl http://localhost:8000/api/alerts/active/
```

### Get Traffic Data
```bash
curl http://localhost:8000/api/traffic/
```

## Continuous Traffic Simulation

Run the simulator in the background to continuously update vehicle data:

```bash
# Terminal 1 - Run development server
python manage.py runserver

# Terminal 2 - Run continuous simulator (simulates 30 minutes of data every ~3 seconds)
python manage.py simulate_traffic --vehicles 30 --duration 1800 --interval 1
```

This makes the data appear to flow naturally as you interact with the dashboard.

## Admin Interface

Access Django Admin at `http://localhost:8000/admin/`

- Login with superuser credentials created during setup
- View/edit vehicles, stations, alerts, and trips
- Manage users and permissions

## Useful Commands

```bash
# View all vehicles in database
python manage.py shell
>>> from ev_tracking.models import EVVehicle
>>> EVVehicle.objects.count()

# Delete all test data
python manage.py shell
>>> from ev_tracking.models import *
>>> EVVehicle.objects.all().delete()
>>> ChargingStation.objects.all().delete()
>>> Alert.objects.all().delete()

# Create specific vehicle
>>> vehicle = EVVehicle.objects.create(
...     vehicle_type='Tesla Model 3',
...     battery_capacity=75,
...     current_charge=50,
...     latitude=37.7749,
...     longitude=-122.4194
... )

# Exit shell
>>> exit()
```

## Troubleshooting

### Port 8000 Already in Use
```bash
python manage.py runserver 8001
```
Then access at `http://localhost:8001`

### Database Locked Error
```bash
# Reset database (development only)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### API Returns 404
Make sure the development server is running and check the URL format.

## Next Steps

1. **Modify Vehicle Routes**: Edit `simulate_traffic.py` to change starting locations
2. **Add More Stations**: Use Django admin to add charging stations
3. **Configure Alerts**: Modify alert thresholds in `views.py`
4. **Deploy**: See README.md for production deployment guide

## Key Files to Customize

- **Models** - `ev_tracking/models.py` - Add new data types
- **APIs** - `ev_tracking/views.py` - Add new endpoints
- **Templates** - `templates/*.html` - Customize UI
- **Settings** - `ev_management/settings.py` - Configure Django

## Performance Tips

- For 1000+ vehicles, use PostgreSQL instead of SQLite
- Enable query caching in settings.py
- Use Redis for session storage
- Consider Celery for async tasks

## Support

Check API documentation at `/api/` endpoint or read README.md for detailed information.
