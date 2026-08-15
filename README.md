<<<<<<< HEAD
# AI-Based EV Traffic & Charging Management System for Expressways

A comprehensive Django-based platform for real-time tracking, management, and optimization of electric vehicles on expressways with intelligent routing and charging station location services.

## Features

### MVP Features (Phase 1)
- **Real-time EV Tracking**: Live vehicle location and status monitoring on interactive maps
- **Charging Station Finder**: Search and filter available charging stations with availability indicators
- **Route Planner**: Intelligent route suggestions with automatic charging stop recommendations
- **Driver Dashboard**: Real-time alerts, battery status, and fleet overview
- **Admin Dashboard**: Fleet analytics, traffic heatmaps, and vehicle health metrics
- **Mock GPS Simulator**: Realistic traffic data generation for testing and demo

### Technology Stack
- **Backend**: Django 6.0 + Django REST Framework
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML5 + Bootstrap 5 + Vanilla JavaScript
- **Maps**: Leaflet.js + OpenStreetMap
- **Charts**: Chart.js for analytics
- **Task Scheduling**: APScheduler for traffic simulation
- **ML Ready**: Scikit-learn, Pandas, NumPy for future ML features

## Project Structure

```
ev_management/
├── ev_management/          # Django settings
│   ├── settings.py         # Configuration
│   ├── urls.py             # Main URL routing
│   └── wsgi.py             # WSGI config
├── ev_tracking/            # Main app
│   ├── models.py           # Database models
│   ├── views.py            # REST API views
│   ├── serializers.py      # DRF serializers
│   ├── urls.py             # API routes
│   ├── admin.py            # Django admin
│   └── management/
│       └── commands/
│           └── simulate_traffic.py  # Traffic simulator
├── templates/              # HTML templates
│   ├── base.html
│   ├── driver_dashboard.html
│   ├── charging_finder.html
│   ├── route_planner.html
│   └── admin_dashboard.html
├── static/                 # CSS, JS, images
├── manage.py               # Django CLI
├── requirements.txt        # Dependencies
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip or conda

### Quick Start

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Create superuser (admin)**:
   ```bash
   python manage.py createsuperuser
   ```

5. **Start development server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the application**:
   - Driver Dashboard: http://localhost:8000/
   - Charging Finder: http://localhost:8000/charging-finder/
   - Route Planner: http://localhost:8000/route-planner/
   - Admin Dashboard: http://localhost:8000/admin-dashboard/
   - API Documentation: http://localhost:8000/api/

## API Endpoints

### Vehicles
- `GET /api/vehicles/` - List all vehicles
- `GET /api/vehicles/{id}/` - Vehicle details
- `POST /api/vehicles/{id}/update_location/` - Update vehicle GPS and battery
- `GET /api/vehicles/fleet_status/` - Fleet statistics

### Charging Stations
- `GET /api/stations/` - List all stations
- `GET /api/stations/{id}/` - Station details
- `GET /api/stations/nearby/?lat=X&lon=Y&radius=50` - Find nearby stations

### Routes
- `GET /api/routes/` - List routes
- `POST /api/routes/suggest/` - Get route with charging stops

### Alerts
- `GET /api/alerts/` - List all alerts
- `GET /api/alerts/active/` - Get unresolved alerts
- `POST /api/alerts/{id}/resolve/` - Mark alert as resolved

### Traffic
- `GET /api/traffic/` - Traffic snapshots
- `GET /api/traffic/?expressway_section=I-80&ordering=-timestamp` - Filter by section

## Traffic Simulator

Generate realistic mock data for testing and demonstrations.

### Usage

```bash
# Run with default settings (50 vehicles, 1 hour)
python manage.py simulate_traffic

# Custom parameters
python manage.py simulate_traffic --vehicles 100 --duration 7200 --interval 5
```

### Parameters
- `--vehicles`: Number of vehicles to simulate (default: 50)
- `--duration`: Simulation duration in seconds (default: 3600)
- `--interval`: Update interval in seconds (default: 5)

The simulator:
- Creates realistic vehicle movements on SF Bay Area expressways
- Generates battery depletion based on speed and distance
- Triggers alerts for low battery and charging availability
- Records traffic snapshots for analytics

## Models

### EVVehicle
- Driver reference (FK to User)
- Vehicle type and battery info
- Current location (lat/lon) and speed
- Status (idle, driving, charging, maintenance)

### ChargingStation
- Name and location coordinates
- Charger availability and capacity
- Charger type (Level1, Level2, DCFC)

### Alert
- Vehicle reference
- Alert type (low_battery, overheating, etc.)
- Severity levels (low, medium, high)
- Resolution tracking

### TrafficSnapshot
- Expressway section identification
- Vehicle count and average speed
- Congestion level classification

## Real-Time Features

### Polling (10-15s intervals)
- Vehicle locations update
- Fleet status refresh
- Charging station availability

### Alerts
- Low battery warnings
- Charging availability notifications
- Route suggestions
- Emergency alerts

## Future Enhancements (Phase 2)

- ML-based traffic flow prediction using LSTM
- Intelligent load balancing across charging stations
- EV route optimization using TSP solver
- Battery health monitoring and predictive maintenance
- WebSocket for true real-time updates
- User authentication and role management
- Mobile app integration

## Performance Considerations

- Database indexing on frequently queried fields
- API pagination (50 items per page)
- Asynchronous task processing with Celery
- Caching for static data (stations, routes)
- Optimized queries with `select_related` and `prefetch_related`

## Deployment

### Production Setup

1. **Use PostgreSQL** with PostGIS extension for geospatial queries
2. **Configure environment variables**:
   ```
   DEBUG=False
   SECRET_KEY=your-secret-key
   ALLOWED_HOSTS=your-domain.com
   DATABASE_URL=postgresql://user:pass@host/db
   ```

3. **Collect static files**:
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Run with production WSGI** (Gunicorn, uWSGI)
5. **Set up Redis** for caching and Celery tasks
6. **Use nginx** as reverse proxy

### Docker Setup (Optional)
See `Dockerfile` and `docker-compose.yml` in the repo.

## Testing

```bash
# Run tests
python manage.py test

# With coverage
coverage run --source='.' manage.py test
coverage report
```

## Troubleshooting

### Port Already in Use
```bash
# Use different port
python manage.py runserver 0.0.0.0:8001
```

### Database Errors
```bash
# Reset database (dev only)
rm db.sqlite3
python manage.py migrate
```

### API Not Responding
```bash
# Check server logs
tail -f debug.log

# Verify API endpoints
curl http://localhost:8000/api/vehicles/
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and linting
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues, feature requests, or documentation updates, please open an issue in the repository.

## Credits

Built with Django, Leaflet.js, Chart.js, and Bootstrap. Data simulation based on realistic SF Bay Area expressway patterns.
=======
# AI-EV-Traffic-Management
An AI-powered EV management platform for smart charging, route optimization, traffic monitoring, weather insights, and EV user management.
>>>>>>> b266047b11beca1638354428e760c7982d4584dd
