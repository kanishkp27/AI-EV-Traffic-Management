# Extending the EV Management System

Guide for adding new features and capabilities to the system.

## Adding New Models

### 1. Create Model Class
Edit `ev_tracking/models.py`:

```python
class MaintenanceLog(models.Model):
    """Track vehicle maintenance"""
    vehicle = models.ForeignKey(EVVehicle, on_delete=models.CASCADE)
    maintenance_type = models.CharField(max_length=100)
    service_date = models.DateTimeField()
    cost = models.FloatField()
    technician_notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-service_date']
```

### 2. Create Serializer
Add to `ev_tracking/serializers.py`:

```python
class MaintenanceLogSerializer(serializers.ModelSerializer):
    vehicle_detail = EVVehicleSerializer(source='vehicle', read_only=True)
    
    class Meta:
        model = MaintenanceLog
        fields = ['id', 'vehicle', 'vehicle_detail', 'maintenance_type', 
                 'service_date', 'cost', 'technician_notes', 'created_at']
```

### 3. Create ViewSet
Add to `ev_tracking/views.py`:

```python
class MaintenanceLogViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceLog.objects.all()
    serializer_class = MaintenanceLogSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['vehicle', 'maintenance_type']
    ordering = ['-service_date']
```

### 4. Register in URLs
Update `ev_tracking/urls.py`:

```python
router.register(r'maintenance-logs', views.MaintenanceLogViewSet)
```

### 5. Create & Run Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

## Adding API Endpoints

### Custom Action Endpoint

Example: Get vehicles needing maintenance

```python
# In ev_tracking/views.py
class EVVehicleViewSet(viewsets.ModelViewSet):
    # ... existing code ...
    
    @action(detail=False, methods=['get'])
    def needs_maintenance(self, request):
        """Get vehicles with high mileage or age"""
        from django.utils import timezone
        from datetime import timedelta
        
        threshold = timezone.now() - timedelta(days=90)
        vehicles = self.get_queryset().filter(
            maintenance_log__isnull=True
        ) | self.get_queryset().filter(
            maintenance_log__service_date__lt=threshold
        )
        
        serializer = self.get_serializer(vehicles.distinct(), many=True)
        return Response(serializer.data)
```

Access at: `GET /api/vehicles/needs_maintenance/`

## Adding Frontend Pages

### 1. Create Template
Create `templates/maintenance_log.html`:

```html
{% extends 'base.html' %}

{% block title %}Maintenance Log - EV Manager{% endblock %}

{% block extra_js %}
<script>
    function loadMaintenanceLogs() {
        fetch('/api/maintenance-logs/')
            .then(response => response.json())
            .then(data => {
                const tbody = document.getElementById('logs-table');
                tbody.innerHTML = '';
                data.forEach(log => {
                    tbody.innerHTML += `
                        <tr>
                            <td>Vehicle ${log.vehicle}</td>
                            <td>${log.maintenance_type}</td>
                            <td>$${log.cost.toFixed(2)}</td>
                            <td>${new Date(log.service_date).toLocaleDateString()}</td>
                        </tr>
                    `;
                });
            });
    }
    
    document.addEventListener('DOMContentLoaded', loadMaintenanceLogs);
</script>
{% endblock %}

{% block content %}
<div class="container">
    <h1>Maintenance Log</h1>
    <table class="table">
        <thead>
            <tr>
                <th>Vehicle</th>
                <th>Type</th>
                <th>Cost</th>
                <th>Date</th>
            </tr>
        </thead>
        <tbody id="logs-table"></tbody>
    </table>
</div>
{% endblock %}
```

### 2. Add View
Add to `ev_tracking/views.py`:

```python
class MaintenanceLogView(TemplateView):
    template_name = 'maintenance_log.html'
```

### 3. Add URL
Update `ev_tracking/urls.py`:

```python
urlpatterns = [
    # ... existing paths ...
    path('maintenance/', views.MaintenanceLogView.as_view(), name='maintenance-log'),
]
```

### 4. Add Navigation Link
Update `templates/base.html` navbar:

```html
<li class="nav-item">
    <a class="nav-link" href="/maintenance/">Maintenance</a>
</li>
```

## Adding Real-Time Features with WebSockets

### 1. Install Channels
```bash
pip install django-channels channels-redis
```

### 2. Configure Django Settings
Update `ev_management/settings.py`:

```python
INSTALLED_APPS = [
    # ... existing apps ...
    'daphne',  # Must be first
]

ASGI_APPLICATION = 'ev_management.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('redis', 6379)],
        },
    }
}
```

### 3. Create Consumer
Create `ev_tracking/consumers.py`:

```python
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class AlertConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('alerts', self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('alerts', self.channel_name)
    
    async def alert_message(self, event):
        await self.send(text_data=json.dumps(event['message']))
```

### 4. Send Alert via WebSocket
In `ev_tracking/views.py`:

```python
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def update_vehicle_location(request, pk):
    # ... update logic ...
    
    if vehicle.current_charge < 20:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)('alerts', {
            'type': 'alert_message',
            'message': {
                'vehicle_id': vehicle.id,
                'alert': 'Low battery',
                'battery': vehicle.current_charge
            }
        })
```

## Adding Machine Learning

### Traffic Prediction with LSTM

```python
# ev_tracking/ml/traffic_predictor.py
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

class TrafficPredictor:
    def __init__(self, lookback=24):
        self.lookback = lookback
        self.model = None
        self.scaler = MinMaxScaler()
    
    def prepare_data(self, traffic_data):
        """Prepare traffic data for LSTM"""
        scaled = self.scaler.fit_transform(traffic_data.reshape(-1, 1))
        X, y = [], []
        
        for i in range(len(scaled) - self.lookback):
            X.append(scaled[i:i+self.lookback])
            y.append(scaled[i+self.lookback])
        
        return np.array(X), np.array(y)
    
    def train(self, X_train, y_train):
        """Train LSTM model"""
        self.model = Sequential([
            LSTM(50, activation='relu', input_shape=(self.lookback, 1)),
            Dense(25, activation='relu'),
            Dense(1)
        ])
        
        self.model.compile(optimizer='adam', loss='mse')
        self.model.fit(X_train, y_train, epochs=20, batch_size=16)
    
    def predict(self, recent_data):
        """Predict next traffic snapshot"""
        scaled = self.scaler.transform(recent_data.reshape(-1, 1))
        X = scaled[-self.lookback:].reshape(1, self.lookback, 1)
        prediction = self.model.predict(X)
        return self.scaler.inverse_transform(prediction)[0][0]
```

### Use in API
```python
@action(detail=False, methods=['get'])
def traffic_forecast(self, request):
    """Forecast traffic for next hour"""
    from .ml.traffic_predictor import TrafficPredictor
    
    predictor = TrafficPredictor()
    recent_data = TrafficSnapshot.objects.filter(
        expressway_section='I-80 East'
    ).order_by('-timestamp')[:24].values_list('average_speed')
    
    prediction = predictor.predict(np.array(recent_data))
    return Response({'predicted_speed': prediction})
```

## Adding Authentication

### 1. Create Custom User Model
```python
# ev_tracking/models.py
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('driver', 'Driver'),
        ('admin', 'Administrator'),
        ('maintenance', 'Maintenance'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='driver')
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)
```

### 2. Update Settings
```python
# ev_management/settings.py
AUTH_USER_MODEL = 'ev_tracking.CustomUser'
```

### 3. Add Permissions to Views
```python
from rest_framework.permissions import IsAuthenticated

class EVVehicleViewSet(viewsets.ModelViewSet):
    queryset = EVVehicle.objects.all()
    serializer_class = EVVehicleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Only show user's own vehicles"""
        if self.request.user.role == 'admin':
            return EVVehicle.objects.all()
        return EVVehicle.objects.filter(driver=self.request.user)
```

## Performance Optimization

### Add Caching
```python
# ev_tracking/views.py
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

@method_decorator(cache_page(60), name='dispatch')
class ChargingStationViewSet(viewsets.ModelViewSet):
    # Caches station list for 60 seconds
    queryset = ChargingStation.objects.all()
    serializer_class = ChargingStationSerializer
```

### Database Optimization
```python
# ev_tracking/views.py
queryset = EVVehicle.objects.select_related('driver').prefetch_related('trip_set')
```

## Testing

### Unit Tests
```python
# ev_tracking/tests.py
from django.test import TestCase
from .models import EVVehicle, ChargingStation

class EVVehicleTestCase(TestCase):
    def setUp(self):
        self.vehicle = EVVehicle.objects.create(
            vehicle_type='Tesla',
            battery_capacity=75,
            current_charge=50
        )
    
    def test_battery_percentage(self):
        self.assertEqual(self.vehicle.battery_percentage(), 66.67)
```

### API Tests
```python
from rest_framework.test import APITestCase

class VehicleAPITestCase(APITestCase):
    def test_list_vehicles(self):
        response = self.client.get('/api/vehicles/')
        self.assertEqual(response.status_code, 200)
```

Run tests:
```bash
python manage.py test
```

## Deployment Checklist

- [ ] Set DEBUG=False
- [ ] Update SECRET_KEY
- [ ] Configure ALLOWED_HOSTS
- [ ] Setup PostgreSQL with PostGIS
- [ ] Configure Redis for caching
- [ ] Setup environment variables
- [ ] Run collectstatic
- [ ] Setup SSL/HTTPS
- [ ] Configure logging
- [ ] Setup monitoring
- [ ] Create superuser
- [ ] Run migrations on production

## Common Tasks

### Add New Field to Model
```bash
# Add field to model
# Run migration
python manage.py makemigrations
python manage.py migrate
```

### Change API Response Format
Edit `serializers.py` and adjust fields or add custom methods

### Add Search Functionality
```python
from rest_framework.filters import SearchFilter

class EVVehicleViewSet(viewsets.ModelViewSet):
    filter_backends = [SearchFilter]
    search_fields = ['vehicle_type', 'id']
```

### Add Filtering
```python
from django_filters.rest_framework import DjangoFilterBackend

class EVVehicleViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'battery_capacity']
```

## Resources

- Django Documentation: https://docs.djangoproject.com/
- DRF Guide: https://www.django-rest-framework.org/
- Channels Documentation: https://channels.readthedocs.io/
- PostgreSQL & PostGIS: https://www.postgresql.org/
